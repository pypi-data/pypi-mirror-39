from dateutil.parser import parse as parse_dt

PERIOD_START_MIN = [0, 45, 90, 105]


def get_match_unique_name(match_data):
    """
    Get skillcorner unique name for a match

    Args:
        match_data (dict): should come from a request to match endpoint. Includes, date_time, and teams
            (with their short_name)

    Returns:
        str: unique name of the match
    """
    return u'{}_{}_{}'.format(
        parse_dt(match_data['date_time']).strftime('%Y%m%d'),
        match_data['home_team']['short_name'],
        match_data['away_team']['short_name'])


def get_time_from_frame(frame, period, period_start, fps):
    """
    Get time of a frame of the tracking data.

    Args:
        frame (int): frame in the video
        period (int): period of the match (1: first half, 2: second half, 3 and 4 for extra-time) this frame is from
        period_start (int): start frame of the period
        fps (float/int): fps of the video

    Returns:
        str: time of the frame, for instance '01:20:10.12' for 80min 10seconds 12cs

    Raises:
        ValueError: if frame < period_start
    """
    if frame < period_start:
        raise ValueError('frame ({}) should be greater than or equal to period_start ({})'.format(frame, period_start))
    frame_since_period_start = frame - period_start
    period_start_min = PERIOD_START_MIN[period - 1]
    cs = int((frame_since_period_start % fps) * 100 // fps)
    s = int(frame_since_period_start // fps + period_start_min * 60)
    h, remainder = divmod(s, 3600)
    m, s = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:02d}.{:02d}'.format(h, m, s, cs)


def add_period_time(tracking_data, video_data):
    """
    Add period and time to tracking_data, inplace
    It will only add it when the frame comes from an active period (not before match start or at half-time...)

    Args:
        tracking_data (list[dict]): data returned by tracking api endpoint (each element should include a frame key)
        video_data (dict): data returned by video api endpoint (should include fps, and start/end of each half)
    """
    fps = video_data['fps']
    first_half = video_data['first_half']
    second_half = video_data['second_half']
    first_extra_time_period = video_data['first_extra_time_period']
    second_extra_time_period = video_data['second_extra_time_period']

    tracking_data.sort(key=lambda d: d['frame'])
    for d in tracking_data:
        period = None
        time = None
        for i, period_limit in enumerate([first_half, second_half, first_extra_time_period,
                                          second_extra_time_period]):
            # This could be much more efficient
            if (period_limit['start'] and period_limit['start'] <= d['frame'] and
                    (not period_limit['end'] or d['frame'] < period_limit['end'])):
                period = i + 1
                time = get_time_from_frame(d['frame'], period, period_limit['start'], fps)
                break
        d['period'] = period
        d['time'] = time
