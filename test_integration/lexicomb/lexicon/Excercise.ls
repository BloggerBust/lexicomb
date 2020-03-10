{
  user_name := arg0;
  activity := arg1;
  reps := arg2;
  start_hour:=arg3;
  start_minute:=arg4;
  end_hour:=arg5;
  end_minute:=arg6;

  entry_count_result:=0;
  total_reps_result:=1;
  duration_result:=2;
  average_time_result:=3;

  user_record := {};

  ?[Excercise[user_name]]{
    user_record[user_name] := Excercise[user_name];
  }{
    user_record[user_name] := {};
  }

  ?[user_record[user_name][activity]]{
    activity_record := user_record[user_name][activity];
    total_reps := activity_record[total_reps_result] + reps;
    entry_count := activity_record[entry_count_result] + 1;
    duration := activity_record[duration_result];
    average_time := activity_record[average_time_result];
  }{
    activity_record := {};
    user_record[user_name][activity] := activity_record;
    total_reps := reps;
    entry_count := 1;
    duration:=0;
    average_time:=0;
  }

  total_minutes:=end_minute-start_minute;
  total_hours:= end_hour-start_hour + total_minutes/60;
  duration := duration + total_hours;

  activity_record[entry_count_result] := entry_count;
  activity_record[total_reps_result] := total_reps;
  activity_record[duration_result] := duration;
  activity_record[average_time_result] := duration / entry_count;
  return user_record;
}
