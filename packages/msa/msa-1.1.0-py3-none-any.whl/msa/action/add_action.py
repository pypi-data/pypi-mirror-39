from msa import repositories
from msa.services import file_service
from msa.utils import log


def execute(args):
    log.set_config(args)
    file = file_service.add_setting(args.alias, args.file)
    repositories.create(args.alias, file)
    log.restore_config()
