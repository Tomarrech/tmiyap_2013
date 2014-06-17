__author__ = 'issahar'
import os

global SCRIPT_PATH
SCRIPT_PATH = os.getcwd() + "/main.py"


def write_to_cron(line):
    line += '\t' + "root\t" + SCRIPT_PATH
    print "This line will be add to cron tasks:***\n%s***" % line
    try:
        cron = open('./crontab', 'a')  # "/etc/crontab"
        type_backup = raw_input("Input backup type for this task [full/differ/increment]\n$>")
        if type_backup in ['full', 'differ', 'increment']:
            cron.writelines(line+' --'+type_backup+'\n')
        cron.close()
        return True
    except:
        print "Error during writing into cron file."
        return False


def make_timetable():
    want = raw_input("Would u like to make timetable for this script? [y/n]\n$>")

    if want == "y" or want == "yes":  #and os.path.exists(SCRIPT_PATH):
        time_type = raw_input("what kind of time u want to use? [daily,weekly,monthly or extra]\n$>")

        if time_type == "daily":
            hour, minutes = raw_input("Please, type daytime when you want to make backup [hh:mm]\n$>").split(":")
            if int(hour) > 24 or int(minutes) > 59:
                print "time was uncorrected. retry"
                make_timetable()
            else:
                time_line = '\n%s %s * * *' % (minutes, hour)
                if os.path.exists(SCRIPT_PATH):
                    if write_to_cron(time_line):
                        return True
                    else:
                        return False

        elif time_type == "weekly":
            week_day = raw_input("Please, type a day you want to make backups (opt at 7 a.m.) "
                                 "[Mon, Tue, Wed, Thu, Fri, Sat, Sun]\n$>")
            week_days = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}

            if week_days.get(week_day):
                time_line = '\n0 7 * * %s' % week_days[week_day]
                if write_to_cron(time_line):
                    return True
                else:
                    return False
            else:
                print "Week-day format is uncorrected. Try again.."
                make_timetable()

        elif time_type == "monthly":
            month_day = raw_input("Please, type a day you want to make backup.(opt at 7 a.m.) [1-31]\n$>")
            if int(month_day) > 31:
                print "Month-day format is uncorrected. Retry."
                make_timetable()
            else:
                time_line = '\n0 7 %s * *' % month_day
                if write_to_cron(time_line):
                    return True
                else:
                    return False

        elif time_type == "extra":
            print "Input time, when ypu want to make back up in format min:hour:day:month:week_day\n" \
                  "If you want rang, type a-b, if you want any of int, type *\n" \
                  "Ex: 0 12 * 0-12/2 2  - every Wednesday[2] every second month[0-12/2] every day[*] at 12:00"
            time_line = '\n' + raw_input("$>")
            if write_to_cron(time_line):
                return True
            else:
                return False
    else:
        print "ok, continue without timetable..."
        return False

if __name__ == "__main__":

    if make_timetable():
        print "timetable created successfully."
    else:
        print "timetable wasn't created."