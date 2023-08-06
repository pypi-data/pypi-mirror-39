
**Synchronize Jira issues to VSTS (Azure Devops)**  
  
USAGE  
=====  
  
    jira2vsts -c config.yml -l /var/log/jira2vsts.log  

  
  
VALIDATION  
==========  
  
To check that the format of config is valid and the script can connect to the two systems type:  
  

    jira2vsts.py -c config.yml -l /var/log/jira2vsts.log --validate  

  
  
Format of config file  
=====================  
  

    jira:  
      password: {JIRA_PASSWORD}  
      url: {JIRA_FULL_URL}  
      username: {JIRA_USERNAME}  
    projects:  
      {CODE_JIRA_PROJECT}:  
        active: {TRUE_OR_FALSE}
        name: {NAME_OF_VSTS_PROJECT}  
        type: {VSTS_DEFAULT_TYPE}  
        state: {FIRST_VSTS_STATE} 
        states:
          - {LIST_VSTS_STATES_IN_ORDER} 
        area_path: {OPTIONNAL_VSTS_AREA_PATH}  
        iteration_path: {OPTIONNAL_VSTS_ITERATION_PATH}  
        name: cmmi # Optionnal  
        team: {OPTIONNAL_VSTS_TEAM}  
    states:  
      {JIRA_STATE}: {VSTS_STATE}  
    vsts:  
      access_token: {VSTS_ACCESS_TOKEN}  
      url: {VSTS_FULL_URL}

TODOS  
=====  
  
- Add default assignee
- Add default followers
- Add attachments