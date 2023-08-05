import os
import logging


def process_template(project_name, app_name, template_file_path, dest_file_path):
    # sed substitute file for PROJECT_NAME & APP_NAME
    # and copy to dest_file_path
    cmd = f"sed \'s/$APP_NAME/{app_name}/g; s/$PROJECT_NAME/{project_name}/g\' {template_file_path} > {dest_file_path}"
    rcode = os.system(cmd)
    if rcode != 0:
        err = f"failed for: {template_file_path} - {dest_file_path}"
        raise Exception(err)


def cleanup(project_name):
    logging.info(f"removing project dir {project_name}")
    os.system(f"rm -rf {project_name}")
