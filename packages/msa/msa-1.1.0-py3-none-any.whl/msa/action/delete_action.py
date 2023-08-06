from msa import repositories
from msa.services import file_service
from msa.utils import log


def execute(args):
    log.set_config(args)

    setting_to_remove = repositories.find_one(args.setting)

    if setting_to_remove is None:
        print('Setting not found!!!')
        return

    repositories.delete(setting_to_remove[0])
    file_service.remove_setting(setting_to_remove[1])

    log.restore_config()
