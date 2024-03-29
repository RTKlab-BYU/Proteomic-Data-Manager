import os
import time
import pickle
import random
import string
import shutil
import glob
import subprocess

from datetime import datetime, timedelta

from django.conf import settings
from django.core import management
from django.db.models import Q, Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from django.utils.timezone import utc
from django.contrib.auth import get_user_model

from file_manager.models import FileStorage, SampleRecord, \
    SystemSettings,  DataAnalysisQueue
from file_manager.views import CACHE_FILE
import logging


logger = logging.getLogger(__name__)


User = get_user_model()
startTime = time.time()

# Generated default system settings


# # for view recent request (get, not post)
# if SystemSettings.objects.first() is None:

try:
    current_backup_settings = \
        SystemSettings.objects.first().auto_backup_settings
    current_purge_settings = \
        SystemSettings.objects.first().auto_purge_settings
except AttributeError:
    form_data = {
        'facility_name': "My Default"
    }
    SystemSettings.objects.create(**form_data, )
    current_backup_settings = \
        SystemSettings.objects.first().auto_backup_settings
    current_purge_settings = \
        SystemSettings.objects.first().auto_purge_settings
task_list = ["database", "rawfile", "processed_file"]


def hourly_task():
    """_Hourly task_
    """
    logger.info("Hourly task started")
    generate_cache_files()
    backup_task("Hourly")
    logger.info("Hourly task finished")


def daily_task():
    """_Perform daily task_
    """
    logger.info("Daily task started")
    backup_task("Daily")
    auto_purge_task()
    storage_purge_task()
    backup_systemfile()
    logger.info("Daily task finished")


def weekly_task():
    logger.info("Weekly task started")
    backup_task("Weekly")
    logger.info("Weekly task finished")


def monthly_task():
    logger.info("Monthly task started")
    backup_task("Monthly")
    logger.info("Monthly task finished")


def backup_task(time_string):
    """_Perform backup task for raw files, processed file, database files_

    Args:
        time_string (_type_): _Hourly, Daily, Weekly or Monthly_
    """
    for key, value in current_backup_settings.items():
        if value == time_string:  # Perform task if time_string matches setting
            key_list = key.split("_")  # backup_storage_task
            storage_index = int(key_list[-2])
            task_type = int(key_list[-1])

            if storage_index == 0 and task_type == 0:  # backup database to
                # primary storage
                logger.info("backup database")
                management.call_command('dbbackup', '-z', "--clean")
            elif task_type == 0:  # copy lastest database to corresponding
                # folder respectively
                try:
                    current_datafile_list = glob.glob(
                        os.path.join(settings.MEDIA_ROOT,
                                     f"{settings.STORAGE_LIST[0]}"
                                     f"/database_backup/*.gz"
                                     ))
                    current_datafile_list.sort(key=os.path.getmtime)
                    target_datafile = \
                        current_datafile_list[-1].replace(
                            settings.STORAGE_LIST[0],
                            settings.STORAGE_LIST[storage_index],
                            1)
                    if not os.path.isdir(os.path.dirname(target_datafile)):
                        os.makedirs(os.path.dirname(target_datafile))
                    shutil.copy(current_datafile_list[-1], target_datafile)

                except IOError as e:
                    logger.error(f"backup database to "
                                 f"{settings.STORAGE_LIST[storage_index]}"
                                 f" failed, {e}")
            elif task_type == 1:  # backup rawfile
                # uploaded in the last 90 days, hard coded here should be ok
                # not most efficient, step through all recrod to check missing
                # raw backup files, file_type is 0-3 for primary, secondary...
                # see Filestorage in Models for more detail
                # compress to 7z if it's 2 and 3 (remote and offline)
                for record in SampleRecord.objects.filter(
                        uploaded_time__gte=datetime.today()-timedelta(
                        days=90)):
                    is_backup = False
                    for item in record.file_storage_indeces.all():
                        if int(item.file_type) == storage_index+1:
                            is_backup = True
                    if not is_backup:
                        try:
                            if record.newest_raw is None:
                                logger.error(
                                    f"{record.pk} raw contain"
                                    f" no valid newest_raw")
                                continue
                            current_raw = os.path.join(
                                settings.MEDIA_ROOT,
                                record.newest_raw.file_location.name)
                            if bool(current_raw) is False:
                                logger.error(
                                    f"{record.pk} raw newest_raw"
                                    f" doesn't exist")
                                continue
                            # Get file extension
                            file_extension = os.path.splitext(record.newest_raw.file_location.name)[-1]
                            # use the same folder structure as current_raw
                            new_name = os.path.join(f"{settings.STORAGE_LIST[storage_index]}/",
                                                    record.newest_raw.file_location.name.split("/", 1)[1])
                            if storage_index != 1:  # compress to 7z
                                new_name = new_name.replace(
                                    file_extension, ".7z")
                                if os.path.isfile(os.path.join(
                                        settings.MEDIA_ROOT, new_name)):
                                    random_str = "".join(random.choice(
                                        string.ascii_lowercase) for i in range(4))
                                    new_name = new_name.replace(
                                        ".7z", "_" + random_str+".7z")
                                subprocess.run(['7z', 'a',  os.path.join(
                                    settings.MEDIA_ROOT, new_name),
                                    current_raw,
                                    "-mx=9",
                                    "-mmt=2"])
                            else:  # copy directly
                                if os.path.isfile(os.path.join(
                                            settings.MEDIA_ROOT, new_name)):
                                    random_str = "".join(random.choice(
                                        string.ascii_lowercase) for i in range(4))
                                    # get a file extension from the full path
                                    new_name = new_name.replace(
                                        "."+file_extension, "_" + random_str + file_extension)
                                os.makedirs(os.path.dirname(os.path.join(
                                            settings.MEDIA_ROOT, new_name)), exist_ok=True)
                                shutil.copy(current_raw, os.path.join(
                                            settings.MEDIA_ROOT, new_name))

                            if (os.path.isfile(os.path.join(
                                    settings.MEDIA_ROOT, new_name))):
                                FileStorageform = {
                                    "file_location": new_name,
                                    'file_type': storage_index+1
                                }
                                fileStorage_new = FileStorage.objects.create(
                                    **FileStorageform, )
                                record.file_storage_indeces.add(
                                    fileStorage_new)
                                logger.info(
                                    f"{record.pk}_{storage_index}_"
                                    f"{task_type} raw backup finished")
                            else:
                                logger.info(
                                    f"{record.pk}_{storage_index}_"
                                    f"{task_type} raw backup failed")
                        except Exception as err:
                            logger.error(
                                f"{record.pk} raw back up failed, {err}")
            elif task_type == 2:  # backup processed_file
                # processed in the last 90 days, hard coded here should be ok
                # not most efficient, step through all recrod check missing
                for record in DataAnalysisQueue.objects.filter(
                    finish_time__gte=datetime.today()-timedelta(
                        days=90)):
                    if record.finish_time is None:  # not finished running
                        continue
                    is_backup = False
                    for item in record.backup_indeces.all():
                        if int(item.file_type) == storage_index+6:
                            is_backup = True
                    if not is_backup:
                        try:
                            to_tz = timezone.get_default_timezone()

                            finish_time = record.finish_time.astimezone(
                                to_tz)
                            file_year, file_month, file_day = \
                                finish_time.year, \
                                finish_time.month, finish_time.day
                            zip_name = \
                                f"{settings.STORAGE_LIST[storage_index]}/"\
                                f"processqueue/{file_year}/{file_month}/" \
                                f"{file_day}/{record.pk}.7z"
                            if os.path.isfile(os.path.join(
                                    settings.MEDIA_ROOT, zip_name)):
                                random_str = "".join(random.choice(
                                    string.ascii_lowercase) for i in range(4))
                                zip_name = zip_name.replace(
                                    ".7z", "_" + random_str+".7z")

                            for item_name in settings.PROCESS_FILE_LIST:
                                current_url = getattr(record, item_name)
                                if bool(current_url) is not False:
                                    add_file_name = \
                                        os.path.join(
                                            settings.MEDIA_ROOT,
                                            item_name + "-" + current_url.name)
                                    subprocess.run(['7z', 'a',  os.path.join(
                                        settings.MEDIA_ROOT, zip_name),
                                        add_file_name,
                                        "-mx=9", "-mmt=2"])

                            if (os.path.isfile(os.path.join(
                                    settings.MEDIA_ROOT, zip_name))):
                                FileStorageform = {
                                    "file_location": zip_name,
                                    'file_type': storage_index+6
                                }
                                fileStorage_new = FileStorage.objects.create(
                                    **FileStorageform, )
                                record.backup_indeces.add(
                                    fileStorage_new)
                                logger.info(
                                    record.pk,
                                    storage_index, task_type,
                                    "process backup finished")
                            else:
                                logger.error(
                                    record.pk,
                                    storage_index, task_type,
                                    "process backup failed")
                        except Exception as err:
                            logger.error(
                                f"{record.pk} process back up failed, {err}")


def auto_purge_task():
    """_Delete files (cache, raw, processed, attachment) that not related to
    any records (SampleRecord deleted).
    """
    # delete file that not related to any records and old than
    #
    for record in FileStorage.objects.filter(file_type=0,
                                             cache_pkl__isnull=True):
        # delete cahche file that not related to any records (already deleted)
        # type 0
        full_file_path = os.path.join(
            settings.MEDIA_ROOT, record.file_location.name)
        if os.path.isfile(full_file_path):
            os.remove(full_file_path)

        logger.info(
            f"FileStorage {record.pk} pkl file will be purged "
            f"due to no related record.")
        FileStorage.objects.filter(pk=record.pk).delete()

    for record in FileStorage.objects.filter(file_type=5,
                                             attachments__isnull=True):
        # delete attachment  that not related to any records (already deleted)
        # type 5
        full_file_path = os.path.join(
            settings.MEDIA_ROOT, record.file_location.name)
        if os.path.isfile(full_file_path):
            os.remove(full_file_path)

        logger.info(
            f"FileStorage {record.pk} attachment file will be purged "
            f"due to no related record.")
        FileStorage.objects.filter(pk=record.pk).delete()

    # type 3 is remote, 4 if offline, maybe should add 3
    for record in FileStorage.objects.filter(file_type__in=[1, 2],
                                             newest_raw__isnull=True,
                                             storage__isnull=True):
        # delete raw file that not related to any records (already deleted)
        # type 1, 2, type 3 is remote, 4 if offline, maybe should add 3

        full_file_path = os.path.join(
            settings.MEDIA_ROOT, record.file_location.name)
        if os.path.isfile(full_file_path):
            os.remove(full_file_path)
        logger.info(
            f"FileStorage {record.pk} raw file will be purged "
            f"due to no related record.{record.file_location}")

        FileStorage.objects.filter(pk=record.pk).delete()

    for record in FileStorage.objects.filter(file_type__in=[6, 7, 8, 9],
                                             procee_queue_backup=True):
        # delete process file that not related to any records (already deleted)
        # type 6, 7, 8, 9, different storage locations
        full_file_path = os.path.join(
            settings.MEDIA_ROOT, record.file_location.name)
        if os.path.isfile(full_file_path):
            os.remove(full_file_path)
        logger.info(
            f"FileStorage {record.pk} process zip file will be purged "
            f"due to no related record.{record.file_location}")

        FileStorage.objects.filter(pk=record.pk).delete()


def storage_purge_task():
    """_delet old files(database, raw, processed) that exceeed the purge
    critias in the settings, purge_storageindex_tasktype_
    """

    now = datetime.now()

    # purge temp record, only keep for 90 days
    archive_cutoff = now - timedelta(days=int(90))
    for record in SampleRecord.objects.filter(
            uploaded_time__lte=archive_cutoff, is_temp=True):
        logger.info(f"Temp record , {record.record_name} will be purged.")
        SampleRecord.objects.filter(pk=record.pk).delete()

    # purge files specified in the settings
    for key, value in current_purge_settings.items():
        if value is None or value == "" or int(value) == 0:
            continue
        key_list = key.split("_")  # _storage_task
        storage_index = int(key_list[-2])
        task_type = int(key_list[-1])
        if task_type == 0:  # purge old databse file
            try:
                pruge_direct = os.path.join(
                    settings.MEDIA_ROOT,
                    f"{settings.STORAGE_LIST[storage_index]}"
                    f"/database_backup/"
                )
                current_time = time.time()
                if not os.path.exists(pruge_direct):
                    continue
                for f in os.listdir(pruge_direct):
                    creation_time = os.path.getctime(pruge_direct + f)
                    if (current_time - creation_time) // (24 * 3600) \
                            >= int(value):
                        os.remove(pruge_direct + f)
                        logger.info(
                            'database file {} will be removed'.format(f))
            except Exception as e:
                logger.error(f"{e} during removing {f}")
        elif task_type == 1:  # purge old raw file, point newest raw to others
            archive_cutoff = now - timedelta(days=int(value))
            for record in SampleRecord.objects.filter(
                    uploaded_time__lte=archive_cutoff):
                if record.file_storage_indeces.count() <= 1:
                    # won't purge if there is only one raw
                    continue
                for item in record.file_storage_indeces.all():
                    if int(item.file_type) == storage_index+1:
                        try:
                            logger.info(
                                f"purge condition met, {item.file_location}"
                                f" will be purged.")

                            file_full_path = os.path.join(
                                settings.MEDIA_ROOT, item.file_location.name)
                            if os.path.isfile(file_full_path):
                                os.remove(file_full_path)
                        except Exception as error:
                            logger.error(
                                f"{error}  while "
                                f"removing {item.pk}-{item.file_location}")
                        finally:
                            if record.newest_raw == item:
                                FileStorage.objects.filter(
                                    pk=item.pk).delete()
                                all_storage = \
                                    record.file_storage_indeces.all()
                                if all_storage.count():
                                    next_newest = all_storage[0]
                                else:
                                    continue
                                SampleRecord.objects.filter(
                                    pk=record.pk).update(
                                    newest_raw=next_newest)
                            else:
                                FileStorage.objects.filter(
                                    pk=item.pk).delete()

        elif task_type == 2:  # purge old process file
            archive_cutoff = now - timedelta(days=int(value))
            for record in DataAnalysisQueue.objects.filter(
                    finish_time__lte=archive_cutoff):
                if record.finish_time is None:
                    continue
                if int(storage_index) == 0:  # unzip file in each fields
                    logger.info(F"removing process queue {record.pk}'s ")
                    file_list = ["input_file_1", "input_file_2",
                                 "input_file_3", "output_file_1",
                                 "output_file_2", "output_file_3", ]
                    for file_item in settings.PROCESS_FILE_LIST:
                        file_path = getattr(record, file_item).name
                        try:
                            if file_path is None:
                                continue
                            file_full_path = os.path.join(
                                settings.MEDIA_ROOT, file_path)
                            if os.path.isfile(file_full_path):
                                os.remove(file_full_path)
                        except Exception as err:
                            logger.info(F"Error during removing {err}")
                        finally:
                            setattr(record, file_item, None)
                            record.save()
                else:  # zipped file in the backup_indeces
                    for item in record.backup_indeces.all():
                        if int(item.file_type) == storage_index+1:
                            try:
                                logger.info(
                                    f"purge condition met,"
                                    f" {item.file_location}"
                                    f" will be purged.")
                                file_full_path = os.path.join(
                                    settings.MEDIA_ROOT, item.file_location)
                                if os.path.isfile(file_full_path):
                                    os.remove(file_full_path)
                            except Exception as error:
                                logger.error(
                                    f"{error}  while "
                                    f"removing {item.pk}-"
                                    f"{item.file_location}")
                            finally:
                                FileStorage.objects.filter(pk=item.pk).delete()


def backup_systemfile():
    """_Backup all system files to storage as a 7z file_
    """
    sys_file_backup = SystemSettings.objects.first().systemfile_backup_settings
    if bool(sys_file_backup):
        folder_to_back = os.path.join(
            settings.MEDIA_ROOT,
            f"{settings.STORAGE_LIST[0]}/systemfiles")
        target_file = os.path.join(
            settings.MEDIA_ROOT,
            f"{sys_file_backup['system_file_backup_target']}"
            f"/system_file_backups/backup_{datetime.now().strftime('%A')}.7z")

        check_folder = os.path.isdir(os.path.dirname(target_file))
        if not check_folder:
            os.makedirs(os.path.dirname(target_file))
        if os.path.isfile(target_file):
            os.remove(target_file)

        subprocess.run(['7z', 'a',  target_file, folder_to_back,
                        "-mx=9", "-mmt=2"])
    logger.info(f"System file backup finished. {target_file}")


def generate_cache_files():
    """_Generate cache files for the dashboard page used in the views_
    """
    data_daily = SampleRecord.objects.all().annotate(date=TruncDay(
        'acquisition_time')).values("date").annotate(
        created_count=Count('id')).order_by("-date")
    data_monthly = SampleRecord.objects.all().annotate(month=TruncMonth(
        'acquisition_time')).values("month").annotate(
        created_count=Count('id')).order_by("-month")
    by_user = SampleRecord.objects.all().values("record_creator_id").annotate(
        total=Count('record_creator_id')).order_by('-total')
    daily_data = []
    daily_lables = []
    monthly_data = []
    monthly_lables = []
    user_names = []
    user_counts = []
    for n in range(0, 30):
        try:
            if data_daily[29-n]["date"] is not None:
                daily_lables.append(
                    data_daily[29-n]["date"].strftime("%B-%d-%Y"))
                daily_data.append(data_daily[29-n]["created_count"])
        except IndexError:
            logger.error(f"Less than {29-n} days of data")
    for n in range(0, 12):
        try:
            if data_monthly[11-n]["month"] is not None:
                monthly_lables.append(
                    data_monthly[11-n]["month"].strftime("%B-%Y"))
                monthly_data.append(data_monthly[11-n]["created_count"])
        except IndexError:
            logger.error(f"Less than {11-n} month of data")
    for item in by_user[:10]:
        if item["record_creator_id"] is not None:
            user_names.append(User.objects.get(
                id=int(item["record_creator_id"])).username)
            user_counts.append(item["total"])

    total, used, free = shutil.disk_usage(
        os.path.join(settings.MEDIA_ROOT,
                     f"{settings.STORAGE_LIST[0]}/"))

    try:
        back_total, back_used, back_free = \
            shutil.disk_usage(os.path.join(settings.MEDIA_ROOT,
                                           f"{settings.STORAGE_LIST[1]}/"))
    except OSError:
        # prevent error while debug on other systems
        back_total, back_used, back_free = 1*(2**30), 1*(2**30), 1*(2**30)

    try:
        remote_total, remote_used, remote_free = shutil.disk_usage(
            os.path.join(settings.MEDIA_ROOT,
                         f"{settings.STORAGE_LIST[2]}/"))
    except OSError:
        # prevent error while debug on other systems
        remote_total, remote_used, remote_free = 1 * \
            (2**30), 1*(2**30), 1*(2**30)

    try:
        offline_total, offline_used, offline_free = shutil.disk_usage(
            os.path.join(settings.MEDIA_ROOT,
                         f"{settings.STORAGE_LIST[3]}/"))
    except OSError:
        # prevent error while debug on other systems
        offline_total, offline_used, offline_free = 1 * \
            (2**30), 1*(2**30), 1*(2**30)
    cached_data = {
        "records": SampleRecord.objects.count(),
        "users": User.objects.count(),
        "time": int((time.time() - startTime)/3600),
        "total": int(total // (2**30)),
        "used": int(used // (2**30)),
        "free": int(free // (2**30)),
        "percent": int(free/total*100),
        'labels': ["used", "free"],
        'data': [int(used // (2**30)), int(free // (2**30))],
        "back_total": int(back_total // (2**30)),
        "back_used": int(back_used // (2**30)),
        "back_free": int(back_free // (2**30)),
        "back_percent": int(back_free/back_total*100),
        'back_labels': ["used", "free"],
        'back_data': [int(back_used // (2**30)), int(back_free // (2**30))],
        'remote_labels': ["used", "free"],
        'remote_data': [int(remote_used // (2**30)),
                        int(remote_free // (2**30))],
        'offline_labels': ["used", "free"],
        'offline_data': [int(offline_used // (2**30)),
                         int(offline_free // (2**30))],
        'daily_data': daily_data,
        'daily_labels': daily_lables,
        'monthly_data': monthly_data,
        'monthly_labels': monthly_lables,
        'user_data': user_counts,
        'user_labels': user_names,
    }
    with open(CACHE_FILE, 'wb') as handle:
        pickle.dump(cached_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# generate cache files on startup when uncommented, can affect debug speed as
# it takes a few seconds to generate
# generate_cache_files()
