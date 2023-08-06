import boto3, botocore, click
import os.path
import colorama as c

class Trapeze :

    def __init__(self, app_name, bucket) :
        c.init()
        self.s3 = boto3.client("s3")
        self.app_name = app_name
        self.bucket = bucket
        self.files = []

    def get_files(self) :
        files = self.s3.list_objects(Bucket = self.bucket, Prefix = self.app_name)
        return files

    def add_files(self, file_paths) :
        self.files = file_paths

    def push(self) :
        for f in self.files :
            try :
                key = "{0}/{1}".format(self.app_name, f)
                # exists?
                try :
                    exists = self.s3.head_object(Bucket = self.bucket, Key = key)
                except :
                    exists = None
                path = "{0}/{1}".format(self.bucket, key)
                if not exists or exists and click.confirm(c.Fore.RED + "'{0}' exists. Overwrite?".format(path) + c.Style.RESET_ALL) :
                    self.s3.upload_file(f, self.bucket, key)
                    click.echo("'{0}' written...".format(path))
            except FileNotFoundError :
                click.echo(c.Fore.RED + "File not found ({0}).".format(f) + c.Style.RESET_ALL)

    def pull(self) :
        for f in self.files :
            try :
                # file exists?
                exists = os.path.isfile(f)
                if not exists or exists and click.confirm(c.Fore.RED + "'{0}' exists. Overwrite?".format(f) + c.Style.RESET_ALL) :
                    key = "{0}/{1}".format(self.app_name, f)
                    self.s3.download_file(self.bucket, "{0}/{1}".format(self.app_name, f), f)
                    click.echo("'{0}' written...".format(f))
            except botocore.exceptions.ClientError :
                click.echo(c.Fore.RED + "Could not find remote file ({0}).".format(f) + c.Style.RESET_ALL)
