from divinegift.logger import log_info, log_err, log_warning
from string import Template
import json
import sys
from datetime import datetime
import re
import os
### import sqlalchemy if needed
try:
    from sqlalchemy import create_engine, MetaData, Table
except:
    pass
from mailer import Mailer, Message
### Обратная совместимость отправки сообщений. Скоро будет Depricated ###
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
#########################################################################


datetime_regex = r'20\d{2}(-|\/)((0[1-9])|(1[0-2]))(-|\/)((0[1-9])|([1-2][0-9])|(3[0-1]))(T|\s)(([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])'


class Settings:
    def __init__(self):
        self.settings = {}

    def get_settings(self):
        return self.settings

    def set_settings(self, json_str):
        self.settings = json_str

    def parse_settings(self, file='./settings.conf', encoding='utf-8', log_changes=True):
        """
        Parse settings from file
        :param file: Filename with settings
        :param encoding: Encoding
        :return: None
        """
        json_data = parse_json(file, encoding=encoding)

        if log_changes:
            dict_c = dict_compare(self.settings, json_data)
            added, removed, modified, same = dict_c.values()
            if len(added) > 0:
                for r in list(added):
                    log_warning('Added {}: {}'.format(r, json_data.get(r)))
            if len(removed) > 0:
                for r in list(removed):
                    log_warning('Removed {}: {}'.format(r, self.settings.get(r)))
            if len(modified) > 0:
                for r in list(modified):
                    log_warning('Modified {}: {} -> {}'.format(r, modified.get(r)[0], modified.get(r)[1]))

        self.set_settings(json_data)


def dict_compare(d1, d2):
    """
    Compare 2 dict
    :param d1: First dict to compare
    :param d2: Second dict
    :return: Dict with results of comparing
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])

    result = {'added': list(added), 'removed': list(removed), 'modified': modified, 'same': list(same)}
    return result


def get_conn(db_conn):
    """
    Create connection for SQLAlchemy
    :param db_conn: DB connection (user, password, host, port, db_name, dialect)
    :return: Engine, Connection, Metadata
    """
    if db_conn.get('dialect') == 'mssql+pytds':
        from sqlalchemy.dialects import registry
        registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
    if db_conn.get('db_host') and db_conn.get('db_port'):
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(**db_conn)
    else:
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_name}'.format(**db_conn)
    engine = create_engine(connect_str)
    conn = engine.connect()
    metadata = MetaData()
    return engine, conn, metadata


def get_raw_conn(db_conn):
    """
    Create raw connection for SQLAlchemy
    :param db_conn: DB connection (user, password, host, port, db_name, dialect)
    :return: Connection
    """
    if db_conn.get('dialect') == 'mssql+pytds':
        from sqlalchemy.dialects import registry
        registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")
    if db_conn.get('db_host') and db_conn.get('db_port'):
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(**db_conn)
    else:
        connect_str = '{dialect}://{db_user}:{db_pass}@{db_name}'.format(**db_conn)    
    engine = create_engine(connect_str)
    conn = engine.raw_connection()
    return conn


def close_conn(conn):
    conn.close()


def get_sql(filename, encoding='utf-8'):
    """
    Get sql string from file
    :param filename: File name
    :param encoding: Encoding of file
    :return: String with sql
    """
    file = open(filename, 'r', encoding=encoding)
    sql = file.read()
    file.close()
    return sql


def get_data(sql, db_conn, encoding='utf-8', **kwargs):
    """
    Get raw data from sql data as dict
    :param sql: File with sql which need to execute
    :param db_conn: DB connect creditions
    :param encoding: Encoding of file
    :param kwargs: List with additional data
    :return: Dictionary
    """
    if os.path.exists(sql):
        script_t = Template(get_sql(sql, encoding))
    else:
        script_t = Template(sql)
    script = script_t.safe_substitute(**kwargs)
    #print(script)

    engine, conn, metadata = get_conn(db_conn)
    res = conn.execute(script)
    ress = [dict(row.items()) for row in res]
    close_conn(conn)

    return ress


def run_script(sql, db_conn, encoding='utf-8', **kwargs):
    """
    Run custom script
    :param sql: File with sql which need to execute
    :param db_conn: DB connect creditions
    :param encoding: Encoding of file
    :param kwargs: List with additional data
    :return: None
    """    
    if os.path.exists(sql):
        script_t = Template(get_sql(sql, encoding))
    else:
        script_t = Template(sql)
    script = script_t.safe_substitute(**kwargs)

    engine, conn, metadata = get_conn(db_conn)
    conn.execute(script)
    close_conn(conn)


def get_args():
    """
    Get dict of args by pairs (e.g. --log_level 'INFO')
    :return: dict of args
    """
    args = sys.argv[1:]
    args_d = {}
    for i, arg in enumerate(args[::2]):
        if i == len(args):
            break
        args_d[arg] = args[i * 2 + 1]
    args_d['name'] = sys.argv[0]
    return args_d


def get_log_param(args):
    """
    Get log_level and log_name from args
    :param args: dict of args from get_args()
    :return: log_level and log_name for set_loglevel()
    """
    log_level = None
    log_name = None
    log_dir = None
    for key in args.keys():
        if key in ['--log_level', '-ll']:
            log_level = args.get(key)
        if key in ['--log_name', '-ln']:
            log_name = args.get(key)
        if key in ['--log_dir', '-ld']:
            log_dir = args.get(key)

    if not log_level:
        log_level = 'INFO'
    if not log_name:
        log_name = None
    if not log_dir:
        log_dir =os.path.join(get_base_dir(), 'logs')

    log_params = {'log_level': log_level, 'log_name': log_name, 'log_dir': log_dir}

    return log_params


def get_base_dir():
    try:
        base_dir = os.getcwd()
    except:
        base_dir = ''

    return base_dir


def parse_json(json_fname, encoding='utf-8'):
    """
    Parse json file
    :param json_fname: filename which should be parsed
    :param encoding: Encoding
    :return: Dict with json data
    """
    try:
        json_file = open(json_fname, encoding=encoding)
        json_str = json_file.read()
        json_data = json.loads(json_str, object_hook=date_hook)
    except:
        json_data = None

    return json_data


def date_hook(json_dict):
    """
    Hook which used for translate date string in json file to datetime type
    :param json_dict: dict from json file
    :return: dict from json after translating
    """
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict


def create_json(json_fname, json_data, encoding='utf-8'):
    """
    Create json file from dict
    :param json_fname: Filename
    :param json_data: Dict which contain data to writing
    :param encoding: Encoding
    :return:
    """
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    with open(json_fname, 'w', encoding=encoding) as outfile:
        response = json.dump(json_data, outfile, ensure_ascii=False, default=dthandler, indent=4)


def send_email_with_attachments(subject, body_text, to_emails, cc_emails, files, file_path,
                                host="mail.s7.ru", from_addr="noreply@s7.ru"):
    """
    Send an email with an attachment
    """
    log_info('Send email with subject {}'.format(subject))

    filelist = get_list_files(file_path, filter=files, add_path=True)

    send_email(body_text, subject, to_emails, CC=cc_emails, FROM=from_addr, HOST=host,
               attachments=filelist)


def send_email_with_attachments_old(subject, body_text, to_emails, cc_emails, files, file_path,
                                host="mail.s7.ru", from_addr="noreply@s7.ru"):
    """
    Send an email with an attachment
    """
    # create the message
    log_info('Send email with subject {}'.format(subject))
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    #if body_text:
    #    msg.attach(MIMEText(body_text))

    msg["To"] = ', '.join(to_emails)
    msg["cc"] = ', '.join(cc_emails)

    for file_to_attach in files:
        try:
            attachment = MIMEBase('application', "octet-stream")

            with open(file_path + file_to_attach, "rb") as fh:
                data = fh.read()

            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            #attachment.add_header(*header)
            attachment.add_header('Content-Disposition', 'attachment; filename={}'.format(file_to_attach))
            msg.attach(attachment)
        except IOError:
            msgs = "Error opening attachment file %s" % file_to_attach
            log_err(msgs)
            #sys.exit(1)

    msg.attach(MIMEText(body_text, 'html'))

    emails = to_emails + cc_emails
    server = smtplib.SMTP(host)
    server.sendmail(from_addr, emails, msg.as_string())

    server.quit()
    log_info('Email was sended')


def send_email(msg, subject, TO, CC=None, BCC=None, FROM='noreply@s7.ru', HOST='mail.s7.ru',
               attachments=None, charset='utf8', IS_HTML=True):
    message = Message(From=FROM,
                      To=TO,
                      Cc=CC,
                      Bcc=BCC,
                      charset=charset)
    message.Subject = subject
    if IS_HTML:
        message.Html = msg
    else:
        message.Body = msg
    if attachments:
        if type(attachments) == list:
            for file in attachments:
                try:
                    message.attach(file)
                except Exception as ex:
                    log_err('Could not attach file: {}'.format(file))
        elif type(attachments) == str:
            try:
                message.attach(attachments)
            except Exception as ex:
                log_err('Could not attach file: {}'.format(attachments))
        else:
            log_warning('There is incorrect type of variable attachments')
    sender = Mailer(HOST)
    sender.send(message)


def get_list_files(path, filter=None, add_path=False, path2=''):
    """
    Get filelist with path in folder
    :param path: Folder containing files
    :param filter: filter (regexp-like), could be list of str or just str. None by default
    :param add_path: bool, will needed add path to file or not
    :param path2: path which need to add
    :return: return list of files with/without path to it
    """
    list_files = []
    if add_path:
        if path2 == '':
            path2 = path
    else:
        path2 = ''

    if filter:
        if type(filter) == list:
            for f in filter:
                list_files.extend([os.path.join(path2, x) for x in os.listdir(path) if re.search(f, x)])
        if type(filter) == str:
            list_files = [os.path.join(path2, x) for x in os.listdir(path) if re.search(filter, x)]
    else:
        list_files = [os.path.join(path2, x) for x in os.listdir(path)]

    return list_files


if __name__ == '__main__':
    pass
