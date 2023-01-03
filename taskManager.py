import os
import win32com.client
import support

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()
root_folder = scheduler.GetFolder('\\')

def addToAutostart(self):
    task_def = scheduler.NewTask(0)
    location = str(support.getCurrentPath())

    # Создаем триггер
    TASK_TRIGGER_LOGON = 9
    trigger = task_def.Triggers.Create(TASK_TRIGGER_LOGON)
    trigger.Id = "LogonTriggerId"
    trigger.UserId = os.environ.get('USERNAME') # получаем имя текущего пользователя
    
    # Добавляем к нему действие
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = self.config.getName()
    action.Path = location + '\\' + self.config.getName() + '.exe'
    action.WorkingDirectory = location

    # Выставляем параметры запуска
    task_def.Settings.Enabled = True
    task_def.Settings.Compatibility = 4
    task_def.Settings.ExecutionTimeLimit = 'PT0S'
    task_def.Settings.AllowHardTerminate = True
    task_def.Settings.IdleSettings.StopOnIdleEnd = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Principal.RunLevel = 1

    # Регистрируем таск, если есть — обновляем
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        self.config.getName(),
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # Без пользователя
        '',  # Без пароля
        TASK_LOGON_NONE)

def removeFromAutostart(self):
    if checkThatAutostartIsActive(self):
        root_folder.DeleteTask(self.config.getName(), 0)

# Проверим на наличие таска
# Да, есть метод получения одного таска по имени, но он падает если таска нет,
# а завязываться на состояние «я упал» как-то не хочется, потому просто посмотрим
# в общем списке
def checkThatAutostartIsActive(self):
    tasks = root_folder.GetTasks(0)
    task_name = self.config.getName()

    is_task_exist = bool(len(list(filter(lambda task: (task.name == task_name), tasks))))

    return is_task_exist

if __name__ == "__main__":
    print(checkThatAutostartIsActive())