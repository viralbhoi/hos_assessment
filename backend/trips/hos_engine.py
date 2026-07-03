def simulate_truck_trip(total_miles, current_cycle_used, avg_speed=60):
    days_log = []
    stops_data = [] # NEW: Track map pins
    miles_remaining = total_miles
    hours_driven_since_fuel = 0.0
    cycle_hours_accumulated = current_cycle_used 
    
    current_day = 1
    is_first_day = True
    
    while miles_remaining > 0 or is_first_day:
        day_timeline = []
        current_time = 0.0
        
        if cycle_hours_accumulated >= 70.0:
            day_timeline.append({"start": 0.0, "end": 24.0, "status": "Off Duty"})
            days_log.append({"day": current_day, "timeline": day_timeline})
            
            # Record a 34-hour restart stop
            stops_data.append({"type": "34-Hour Restart", "mile_mark": total_miles - miles_remaining})
            
            current_day += 1
            cycle_hours_accumulated = 0.0
            continue
        
        if is_first_day:
            day_timeline.append({"start": 0.0, "end": 6.0, "status": "Off Duty"})
            day_timeline.append({"start": 6.0, "end": 7.0, "status": "On Duty"}) 
            stops_data.append({"type": "Pickup", "mile_mark": 0}) # Pickup location
            current_time = 7.0
            cycle_hours_accumulated += 1.0
            is_first_day = False
        else:
            day_timeline.append({"start": 0.0, "end": 10.0, "status": "Sleeper Berth"}) 
            stops_data.append({"type": "Hotel / Sleeper", "mile_mark": total_miles - miles_remaining})
            current_time = 10.0
            
        day_driving_window_start = current_time 
        day_driving_accumulated = 0.0
        consecutive_driving_streak = 0.0
        
        while current_time < 24.0 and miles_remaining > 0:
            if (current_time - day_driving_window_start) >= 14.0 or day_driving_accumulated >= 11.0 or cycle_hours_accumulated >= 70.0:
                break
                
            if consecutive_driving_streak >= 8.0:
                break_end = min(current_time + 0.5, 24.0)
                day_timeline.append({"start": current_time, "end": break_end, "status": "Off Duty"})
                stops_data.append({"type": "30-Min Rest", "mile_mark": total_miles - miles_remaining})
                current_time = break_end
                consecutive_driving_streak = 0.0
                continue
                
            if hours_driven_since_fuel >= (1000 / avg_speed):
                fuel_end = min(current_time + 0.5, 24.0)
                day_timeline.append({"start": current_time, "end": fuel_end, "status": "On Duty"})
                stops_data.append({"type": "Fuel Station", "mile_mark": total_miles - miles_remaining})
                time_spent = fuel_end - current_time
                cycle_hours_accumulated += time_spent
                current_time = fuel_end
                hours_driven_since_fuel = 0.0
                continue

            time_left_in_window = 14.0 - (current_time - day_driving_window_start)
            time_left_in_drive_cap = 11.0 - day_driving_accumulated
            time_to_next_mandatory_break = 8.0 - consecutive_driving_streak
            time_left_in_cycle = 70.0 - cycle_hours_accumulated
            
            sim_step = min(0.5, time_left_in_window, time_left_in_drive_cap, time_to_next_mandatory_break, time_left_in_cycle)
            hours_to_finish_trip = miles_remaining / avg_speed
            
            if hours_to_finish_trip <= sim_step:
                drive_end = current_time + hours_to_finish_trip
                day_timeline.append({"start": current_time, "end": drive_end, "status": "Driving"})
                cycle_hours_accumulated += hours_to_finish_trip
                
                if cycle_hours_accumulated + 1.0 <= 70.0:
                    drop_end = min(drive_end + 1.0, 24.0)
                    day_timeline.append({"start": drive_end, "end": drop_end, "status": "On Duty"})
                    cycle_hours_accumulated += (drop_end - drive_end)
                    current_time = drop_end
                
                stops_data.append({"type": "Dropoff", "mile_mark": total_miles})
                miles_remaining = 0.0
                break
            else:
                day_timeline.append({"start": current_time, "end": current_time + sim_step, "status": "Driving"})
                current_time += sim_step
                day_driving_accumulated += sim_step
                consecutive_driving_streak += sim_step
                hours_driven_since_fuel += sim_step
                cycle_hours_accumulated += sim_step
                miles_remaining -= (sim_step * avg_speed)
                
        if current_time < 24.0:
            day_timeline.append({"start": current_time, "end": 24.0, "status": "Sleeper Berth"})
            
        days_log.append({
            "day": current_day,
            "timeline": day_timeline,
        })
        current_day += 1
        
    return days_log, stops_data