from msa import repositories
from msa.services import file_service
from msa.utils import log


def execute(args):
    log.set_config(args)

    selected_setting = repositories.find_selected()
    setting_to_use = repositories.find_one(args.setting)

    if setting_to_use is None:
        print('Setting not found!!!')
        return

    if selected_setting is not None:
        repositories.update(selected_setting[0], 0)
        file_service.deactivate_setting(selected_setting[1])

    repositories.update(setting_to_use[0], 1)
    file_service.activate_setting(setting_to_use[1])

    log.restore_config()
