import pkr_Interface

if __name__ == '__main__':
    sql = """SELECT * FROM t_command_list WHERE cmd_type = %s;"""
    db = pkr_Interface.db_controller()
    result = db.get_SingleValue(sql, "nmap")
    print(result)