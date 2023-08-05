from dataflows import Flow, load, PackageWrapper, add_metadata
from datapackage_pipelines_ckanext import helpers as ckanext_helpers
from oauth2client.client import OAuth2Credentials
from googleapiclient.discovery import build
from httplib2 import Http
from os import path
from os import makedirs
import json
from base64 import urlsafe_b64decode
from collections import defaultdict
from utils import temp_loglevel


def get_allowed_senders(resource):
    for row in resource:
        yield {'from_address': row['from_address'].lower().strip(),
               'to_address': row['to_address'].lower().strip(),
               'organization_id': row['organization_id'].strip()}


def is_email_match(a, b):
    return '<{}>'.format(a) in b or '<{}>'.format(b) in a or a == b


def get_sender_organization_id(from_email, to_email, allowed_senders, config):
    if from_email and to_email:
        from_email = from_email.lower().strip()
        to_email = to_email.lower().strip()
        for row in allowed_senders:
            if is_email_match(from_email, row['from_address']) and is_email_match(to_email, row['to_address']):
                return row['organization_id']
        default_sender_to_address = config.get('default_sender_to_address')
        default_sender_organization_id = config.get('default_sender_organization_id')
        if default_sender_to_address and default_sender_organization_id:
            default_sender_to_address = default_sender_to_address.lower().strip()
            if is_email_match(to_email, default_sender_to_address):
                return default_sender_organization_id
    return None


def get_messages(source_stats, allowed_senders):
    stats = defaultdict(int)
    config = ckanext_helpers.get_plugin_configuration('upload_via_email')
    credentials = OAuth2Credentials.from_json(config['gmail_token'])
    data_path = config['data_path']
    assert credentials and not credentials.invalid
    attachments_path = path.join(data_path, 'attachments')
    with temp_loglevel():
        service = build('gmail', 'v1', http=credentials.authorize(Http()), cache_discovery=False)
        results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    for message in results.get('messages', []):
        message_id = message['id']
        with temp_loglevel():
            service.users().messages().modify(id=message_id, userId='me', body={'removeLabelIds': ['UNREAD']}).execute()
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        headers = {header['name']: header['value']
                   for header in message.get('payload', {}).get('headers', [])
                   if header.get('name') and header.get('value')}
        organization_id = get_sender_organization_id(headers.get('From'), headers.get('To'), allowed_senders, config)
        if organization_id:
            makedirs(path.join(attachments_path, message_id), exist_ok=True)
            part_ids = []
            for part in message.get('payload', {}).get('parts', []):
                part_id = part['partId']
                part_ids.append(part_id)
                with open(path.join(attachments_path, message_id, 'part{}.body'.format(part_id)), 'wb') as f:
                    body = part.get('body', {})
                    if 'attachmentId' in body:
                        with temp_loglevel():
                            attachment = service.users().messages().attachments().get(userId='me', messageId=message_id,
                                                                                      id=body['attachmentId']).execute()
                        data = attachment['data']
                    else:
                        data = body.pop('data', '')
                    f.write(urlsafe_b64decode(data))
                with open(path.join(attachments_path, message_id, 'part{}.json'.format(part_id)), 'w') as f:
                    json.dump(part, f, indent=2)
            yield {'id': message_id,
                   'snippet': message.get('snippet', ''),
                   'from': headers.get('From', ''),
                   'to': headers.get('To', ''),
                   'date': headers.get('Date', ''),
                   'subject': headers.get('Subject', ''),
                   'part_ids': part_ids,
                   'organization_id': organization_id}
            with open(path.join(attachments_path, message_id, 'message.json'), 'w') as f:
                json.dump(message, f, indent=2)
            stats['downloaded_messages: downloaded'] += 1
        else:
            stats['download_messages: unauthorized'] += 1
    source_stats.update(**stats)


def flow(parameters, datapackage, resources, source_stats):

    def download_messages(package: PackageWrapper):
        if 'allowed-senders' in package.pkg.resource_names:
            package.pkg.remove_resource('allowed-senders')
        package.pkg.add_resource({'dpp:streaming': True,
                                  'name': 'messages',
                                  'path': 'messages.csv',
                                  'schema': {'fields': [{'name': 'id', 'type': 'string'},
                                                        {'name': 'snippet', 'type': 'string'},
                                                        {'name': 'from', 'type': 'string'},
                                                        {'name': 'to', 'type': 'string'},
                                                        {'name': 'date', 'type': 'string'},
                                                        {'name': 'subject', 'type': 'string'},
                                                        {'name': 'part_ids', 'type': 'array'},
                                                        {'name': 'organization_id', 'type': 'string'}]}})
        yield package.pkg
        allowed_senders = []
        for resource in package:
            if resource.res.name == 'allowed-senders':
                allowed_senders = list(get_allowed_senders(resource))
            else:
                yield resource

        yield get_messages(source_stats, allowed_senders)

    return Flow(add_metadata(name='_'),
                load((datapackage, resources)),
                download_messages)
