import subprocess
import logging

logging.basicConfig(filename='auto_alembic.log', encoding='utf-8', level=logging.DEBUG)

def alembic_check_changes():
    str_arguments = []
    CMD = "alembic check"
    p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        str_arguments.append(line)
        logging.info(line)
    retval = p.wait()
    check_message:str = str(str_arguments[str_arguments.__len__()-1])

    return check_message

def alembic_revision_generate(commit_message:str):
    str_arguments = []
    CMD = 'alembic revision --autogenerate -m "'
    CMD += str(commit_message + '"')

    p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p.stdout.readlines():
        str_arguments.append(line)
        logging.info(line)
    retval = p.wait()
    check_message:str = str(str_arguments[str_arguments.__len__()-1])

    check_message

    if "Generating" in check_message and "done" in check_message:
        return True
    else:
        return False

def alembic_apply():
    
    CMD = 'alembic upgrade head'
    
    str_arguments = []

    p = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        str_arguments.append(line)
        logging.info(line)
    retval = p.wait()

    if "Running upgrade" in str(str_arguments[str_arguments.__len__()-1]):
        tmp_info = alembic_check_changes()
        if "No new upgrade operations detected." in tmp_info:
            return True
        else:
            return False
    else:
        return False

def alembic_changes_detected(check_message:str):
    if "New upgrade operations detected:" in check_message:
        return True
    else:
        return False

def alembic_generate_commit_message(check_message:str):
    start = check_message.index("d: ") +3

    substring = str(check_message[start:check_message.__len__()-1])
    
    num_of_colums_edited = 0
    num_of_modify_edited = 0
    num_of_removed = 0

    colunm_add = False
    colunm_modify = False
    colunm_removed = False
    
    num_of_table_removed = 0
    num_of_table_added = 0

    table_removed = False
    table_add = False
    
    edited_tables = []

    for index in range(substring.__len__()-1):
        tmp1 = substring[index:7 + index]
        
        if "add_tab" in tmp1:
            num_of_table_added += 1
            table_add = True

        if "ove_tab" in tmp1:
            num_of_table_removed += 1
            table_removed = True

        if "add_col" in tmp1:
            num_of_colums_edited += 1
            colunm_add = True

        if "ove_col" in tmp1:
            num_of_removed += 1
            colunm_removed = True

        if "modify_" in tmp1:
            num_of_modify_edited += 1
            colunm_modify = True

            stName = index

            for i in substring[index:substring.__len__()-1]:
                stName += 1

                if i == "'":
                    if substring[stName:stName+1] != ",":
                        break

            enName = stName

            for i in substring[stName:substring.__len__()-1]:
                if i == "'":
                    
                    tmp_table = str(substring[stName:enName])
                    
                    if not edited_tables.__contains__(tmp_table):
                        edited_tables.append(tmp_table)
                    
                    break
                enName += 1


        if "table=<" in tmp1:
            end = index
            
            for i in substring[index:substring.__len__()-1]:
                end += 1
                if i == ">":
                    break
            
            table_tmp = substring[index+7:end-1]

            if not edited_tables.__contains__(table_tmp):
                edited_tables.append(table_tmp)

    message = ""

    if table_add:
        message += str("added_" + str(num_of_table_added) + "_tables_")

    if table_removed:
        message += str("removed_" + str(num_of_table_removed) + "_tables_")

    if colunm_add:
        message += str("added_" + str(num_of_colums_edited) + "_colums_")

    if colunm_modify:
        message += str("modified_" + str(num_of_modify_edited) + "_colums_")
        
    if colunm_removed:
        message += str("removed_" + str(num_of_removed) + "_colums_")

    if edited_tables.__len__() == 1:
        message += "on_table_"
    elif edited_tables.__len__() > 1:
        message += "on_tables_"


    for item in edited_tables:
        message += str(item + "_")

    message = message[0:message.__len__()-1]

    return message

def alembic_auto_upgrade(message:str = ""):
    
    cmd_out = alembic_check_changes()

    if alembic_changes_detected(cmd_out):
        if message =="":    
            if alembic_revision_generate(alembic_generate_commit_message(cmd_out)):
                if alembic_apply():
                    return "head upgraded"
                else: return "upgrade errors"
            else: return "errors in generate revision"
        else:
            if alembic_revision_generate(message):
                if alembic_apply():
                    return "head upgraded"
                else: return "upgrade errors"
            else: return "errors in generate revision"

    else: return "not changes detected"