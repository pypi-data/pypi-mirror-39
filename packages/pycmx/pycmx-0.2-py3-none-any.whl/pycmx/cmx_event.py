class CmxEvent:
    def __init__(self,title,number,clip_name,source_name,channels,source_start,source_finish,
            record_start, record_finish, fcm_drop, remarks = [] , unrecognized = []):
        self.title = title
        self.number = number
        self.clip_name = clip_name
        self.source_name = source_name
        self.channels = channels
        self.source_start = source_start
        self.source_finish = source_finish
        self.record_start = record_start
        self.record_finish = record_finish
        self.fcm_drop = fcm_drop
        self.remarks = remarks
        self.unrecgonized = unrecognized


