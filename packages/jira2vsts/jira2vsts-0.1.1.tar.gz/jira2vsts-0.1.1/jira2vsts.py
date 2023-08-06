#!/usr/bin/env python
import logging
import logging.handlers
import os
import time
import traceback
from datetime import datetime
from urllib.parse import urljoin, urlparse

import click as click
import validictory
import yaml
from dateutil.parser import parse
from jira import JIRA
from msrest.authentication import BasicAuthentication
from vsts.build.v4_0.models import JsonPatchOperation
from vsts.vss_connection import VssConnection
from vsts.work_item_tracking.v4_1.models import Wiql

SCHEMA_GLOBAL = {
    "type": "object",
    "properties": {
        "last_sync": {
            "type": "string",
            "required": False,
        },
        "jira": {
            "type": "object",
            "required": False,
            "properties": {
                "url": {
                    "type": "string",
                    "required": True,
                },
                "username": {
                    "type": "string",
                    "required": True,
                },
                "password": {
                    "type": "string",
                    "required": True,
                }
            },
        },
        "vsts": {
            "type": "object",
            "required": False,
            "properties": {
                "access_token": {
                    "type": "string",
                    "required": True,
                },
                "url": {
                    "type": "string",
                    "required": True,
                }

            },
        },
        "projects": {
            "required": True,
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "properties": {
                        "active": {
                            "type": "boolean",
                            "required": True,
                        },
                        "name": {
                            "type": "string",
                            "required": True,
                        },
                        "type": {
                            "type": "string",
                            "required": True,
                            "enum": ['task', 'issue', 'feature', 'requirement'],
                        },
                        "team": {
                            "type": "string",
                            "required": False,
                        },
                        "state": {
                            "type": "string",
                            "required": True,
                            "enum": ['Proposed', 'New'],
                        },
                        "states": {
                            "type": "array",
                            "required": True,
                        },
                        "iteration_path": {
                            "type": "string",
                            "required": False,
                        },
                        "area_path": {
                            "type": "string",
                            "required": False,
                        }
                    },

                },
            },
        },
        "states": {
            "required": True,
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "string",
                },
            },
        },

    }
}


def _create_work_item_field_patch_operation(op, field, value):
    path = '/fields/{field}'.format(field=field)
    patch_operation = JsonPatchOperation()
    patch_operation.op = op
    patch_operation.path = path
    patch_operation.value = value
    return patch_operation


def __validate_and_get_data(config, logger, validate):
    content = open(config, 'r').read()
    try:
        content = yaml.load(content)
        validictory.validate(content, SCHEMA_GLOBAL)
    except:
        if validate:
            click.secho(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()
    logger.info('Format of the config file is valid')
    if validate:
        click.echo('Format of the config file is valid')
    return content


def __get_logger(logfile):
    logger = logging.getLogger('jira2vsts')
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(logfile, 'a', 100000, 10)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def __update_last_sync_to_config(config, data):
    f = open(config, 'w+')
    f.write(yaml.dump(data, default_flow_style=False, allow_unicode=True))
    f.close()


@click.command()
@click.option('--validate', '-v', is_flag=True, default=False, type=click.BOOL)
@click.option('--logfile', '-l', type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=True,
                                                 resolve_path=True, allow_dash=True), required=True)
@click.option('--config', '-c',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True, allow_dash=True), required=True)
@click.pass_context
def cli(ctx, validate, logfile, config):
    """CLI for Jira2Vsts"""
    start = time.time()
    nbr_issues = 0
    logger = __get_logger(logfile)
    data = __validate_and_get_data(config, logger, validate)
    VSTS_URL = data['vsts']['url']
    VSTS_TOKEN = data['vsts']['access_token']
    JIRA_URL = data['jira']['url']
    PROJECTS = data['projects']
    JIRA_PROJECTS = [k for k, v in data['projects'].items() if v['active']]
    JIRA_USERNAME = data['jira']['username']
    JIRA_PASSWORD = data['jira']['password']
    STATES = data.get('states', {})
    LAST_SYNC = data.get('last_sync', None)
    JIRA_BROWSE = urljoin(JIRA_URL, os.path.normpath(urlparse(JIRA_URL).path) + '/browse/%s')
    NOW = datetime.now().isoformat()
    data['last_sync'] = NOW
    try:
        jira = JIRA(JIRA_URL, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
        logger.info('connection successful to jira')
        if validate:
            click.echo('connection successful to jira')
    except:
        if validate:
            click.echo(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()

    try:
        credentials = BasicAuthentication('', VSTS_TOKEN)
        connection = VssConnection(base_url=VSTS_URL, creds=credentials)
        wit_client = connection.get_client(
            'vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient')
        logger.info('connection successful to vsts')
        if validate:
            click.echo('connection successful to vsts')
    except:
        if validate:
            click.echo(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()
    if validate:
        raise click.Abort()

    # STARTING THE PROCESS
    logger.info('start processing after connecting')
    logger.info('Jira projects to process : %s', JIRA_PROJECTS)
    for jira_project in JIRA_PROJECTS:
        FIRST_STATE = PROJECTS[jira_project].get('state')
        PROJECT_STATES = PROJECTS[jira_project].get('states', [])
        vsts_project = PROJECTS[jira_project]['name']
        vsts_type = PROJECTS[jira_project]['type']
        vsts_area_path = PROJECTS[jira_project].get('area_path')
        vsts_iteration_path = PROJECTS[jira_project].get('iteration_path')
        logger.info('starting jira project [%s] to [%s]', jira_project, vsts_project)
        logger.info('last sync is : %s', LAST_SYNC)
        if LAST_SYNC:
            last_sync_formatted = parse(LAST_SYNC).strftime('%Y/%m/%d %H:%M')
            jira_issues = jira.search_issues('project=%s AND updated >= "%s"' % (jira_project, last_sync_formatted))
        else:
            jira_issues = jira.search_issues('project=%s' % jira_project)
        JIRA_ITEMS = {j.key for j in jira_issues}
        logger.info('jira issues to send : %s', JIRA_ITEMS)
        for jira_item in JIRA_ITEMS:
            nbr_issues += 1
            issue = jira.issue(jira_item)
            issue_title = "{} / {}".format(jira_item, issue.fields.summary)
            updated = parse(issue.fields.updated).strftime('%d/%m/%Y %H:%M')
            issue_description = """URL: <a href="{url}" target="_blank">{url}</a>
Rapporteur: {f.reporter}
Mise à jour: {updated}

<strong>ORIGINAL:</strong>
{f.description}
            """.format(i=issue, f=issue.fields, url=JIRA_BROWSE % jira_item, updated=updated)

            wiql = Wiql(
                query="""
                        SELECT [System.Id]
                        FROM WorkItems
                        WHERE 
                        [System.Title] contains "%s" AND
                        [System.TeamProject] = "%s"
                        """ % (jira_item, vsts_project)
            )
            wiql_results = wit_client.query_by_wiql(wiql).work_items
            work_items = (
                wit_client.get_work_item(int(res.id)) for res in wiql_results
            )
            vsts_id = False
            for work_item in work_items:
                workitem_name = work_item.fields.get('System.Title', '')
                if workitem_name and workitem_name.startswith(jira_item):
                    vsts_id = work_item.id
            document = []
            document.append(_create_work_item_field_patch_operation('add', 'System.Title', issue_title))
            document.append(_create_work_item_field_patch_operation('add', 'System.Description',
                                                                    issue_description.replace("\n", "<br />\n")))
            try:
                if not vsts_id:
                    logger.info('create a new work item with state=%s for %s', STATES.get(issue.fields.status.name),
                                jira_item)
                    document.append(_create_work_item_field_patch_operation('add', 'System.State', FIRST_STATE))
                    if vsts_area_path:
                        document.append(
                            _create_work_item_field_patch_operation('add', 'System.AreaPath', vsts_area_path))
                    if vsts_iteration_path:
                        document.append(
                            _create_work_item_field_patch_operation('add', 'System.IterationPath', vsts_iteration_path))
                    workitem = wit_client.create_work_item(project=vsts_project, type=vsts_type, document=document)
                    vsts_id = workitem.id
                else:
                    logger.info('update work item with id=%s, state=%s for %s', vsts_id,
                                STATES.get(issue.fields.status.name),
                                jira_item)
                    workitem = wit_client.update_work_item(id=vsts_id, document=document)
                if issue.fields.status.name in STATES:
                    idx = 0
                    for project_state in PROJECT_STATES:
                        idx += 1
                        if workitem.fields['System.State'] == project_state:
                            break
                    for project_state in PROJECT_STATES[idx:]:
                        if workitem.fields['System.State'] == STATES[issue.fields.status.name]:
                            break
                        document = [_create_work_item_field_patch_operation('add', 'System.State', project_state)]
                        old_state = workitem.fields['System.State']
                        logger.debug('%s - try to pass the state from [%s] to [%s]', jira_item, old_state,
                                     project_state)
                        workitem = wit_client.update_work_item(document=document, id=vsts_id)
                        logger.debug('%s - the state is passed from [%s] to [%s]', jira_item, old_state,
                                     workitem.fields['System.State'])

            except:
                logger.error(traceback.format_exc())
                raise click.Abort()

    logger.info('end processing, nbr_issues=%s time=%s seconds', nbr_issues, round(time.time() - start, 2))
    __update_last_sync_to_config(config, data)


if __name__ == '__main__':
    cli(obj={})


def main():
    return cli(obj={})
