# Fix for Merge Node Errors

## The Problem
The Code nodes are failing because they're trying to access inputs that don't exist yet. In n8n 2.0+, when multiple nodes feed into a Code node, they arrive as separate executions, not as an array.

## Solution: Use Merge Node First

Instead of trying to merge in the Code node, use n8n's **Merge** node to combine the inputs first.

### Step 1: Add Merge Nodes

**For Whoop Data:**
1. Delete the "Merge Whoop Data" Code node
2. Add a **Merge** node (search for "Merge" in node list)
3. Name it "Combine Whoop APIs"
4. Settings:
   - Mode: **Combine**
   - Combination Mode: **Merge By Position**
5. Connect all 3 Whoop nodes to this Merge node:
   - Whoop Recovery → Input 1
   - Whoop Sleep → Input 2  
   - Whoop Cycle → Input 3

**For Oura Data:**
1. Delete the "Merge Oura Data" Code node
2. Add a **Merge** node
3. Name it "Combine Oura APIs"
4. Settings:
   - Mode: **Combine**
   - Combination Mode: **Merge By Position**
5. Connect all 3 Oura nodes:
   - Oura Readiness → Input 1
   - Oura Sleep → Input 2
   - Oura Activity → Input 3

### Step 2: Add Code Nodes After Merge

**After "Combine Whoop APIs" Merge:**
Add a Code node named "Transform Whoop" with this code:

```javascript
// Now we have all 3 responses merged
const items = $input.all();

// Extract data from each API response
const recovery = items.find(item => item.json.records)?.json || {};
const sleep = items.find(item => item.json.records && item.json.records[0]?.score?.sleep_performance_percentage !== undefined)?.json || {};
const cycle = items.find(item => item.json.records && item.json.records[0]?.score?.strain !== undefined)?.json || {};

const merged = {
  user_id: 'partner_a',
  date: new Date().toISOString().split('T')[0],
  // Recovery
  recovery_score: recovery.records?.[0]?.score?.recovery_score,
  hrv_rmssd_milli: recovery.records?.[0]?.score?.hrv_rmssd_milli,
  resting_heart_rate: recovery.records?.[0]?.score?.resting_heart_rate,
  spo2_percentage: recovery.records?.[0]?.score?.spo2_percentage,
  skin_temp_celsius: recovery.records?.[0]?.score?.skin_temp_celsius,
  // Sleep
  sleep_performance_percentage: sleep.records?.[0]?.score?.sleep_performance_percentage,
  sleep_efficiency_percentage: sleep.records?.[0]?.score?.sleep_efficiency_percentage,
  sleep_duration_minutes: sleep.records?.[0]?.score?.total_sleep_duration_milli / 60000,
  rem_sleep_minutes: sleep.records?.[0]?.score?.stage_summary?.total_rem_sleep_milli / 60000,
  deep_sleep_minutes: sleep.records?.[0]?.score?.stage_summary?.total_slow_wave_sleep_milli / 60000,
  light_sleep_minutes: sleep.records?.[0]?.score?.stage_summary?.total_light_sleep_milli / 60000,
  sleep_disturbances: sleep.records?.[0]?.score?.sleep_disturbances,
  // Strain
  day_strain: cycle.records?.[0]?.score?.strain,
  energy_burned_calories: cycle.records?.[0]?.score?.kilojoule / 4.184,
  avg_heart_rate: cycle.records?.[0]?.score?.average_heart_rate,
  max_heart_rate: cycle.records?.[0]?.score?.max_heart_rate
};

return [{json: merged}];
```

**After "Combine Oura APIs" Merge:**
Add a Code node named "Transform Oura" with this code:

```javascript
// Now we have all 3 responses merged
const items = $input.all();

// Extract data from each API response
const readiness = items.find(item => item.json.data && item.json.data[0]?.score !== undefined && item.json.data[0]?.contributors?.temperature_deviation !== undefined)?.json || {};
const sleep = items.find(item => item.json.data && item.json.data[0]?.total_sleep_duration !== undefined)?.json || {};
const activity = items.find(item => item.json.data && item.json.data[0]?.steps !== undefined)?.json || {};

const merged = {
  user_id: 'partner_b',
  date: new Date().toISOString().split('T')[0],
  // Readiness
  readiness_score: readiness.data?.[0]?.score,
  temperature_deviation: readiness.data?.[0]?.contributors?.temperature_deviation,
  hrv_balance: readiness.data?.[0]?.contributors?.hrv_balance,
  // Sleep
  sleep_score: sleep.data?.[0]?.score,
  total_sleep_duration_seconds: sleep.data?.[0]?.total_sleep_duration,
  sleep_efficiency: sleep.data?.[0]?.efficiency,
  rem_sleep_duration_seconds: sleep.data?.[0]?.rem_sleep_duration,
  deep_sleep_duration_seconds: sleep.data?.[0]?.deep_sleep_duration,
  light_sleep_duration_seconds: sleep.data?.[0]?.light_sleep_duration,
  sleep_latency_seconds: sleep.data?.[0]?.latency,
  restlessness: sleep.data?.[0]?.restless_periods,
  // Activity
  activity_score: activity.data?.[0]?.score,
  steps: activity.data?.[0]?.steps,
  active_calories: activity.data?.[0]?.active_calories,
  total_calories: activity.data?.[0]?.total_calories,
  met_minutes_high: activity.data?.[0]?.high_activity_met_minutes,
  met_minutes_medium: activity.data?.[0]?.medium_activity_met_minutes,
  met_minutes_low: activity.data?.[0]?.low_activity_met_minutes
};

return [{json: merged}];
```

### Step 3: Connect the Flow

**Whoop path:**
```
Whoop Recovery ┐
Whoop Sleep    ├→ Combine Whoop APIs → Transform Whoop → Save Whoop
Whoop Cycle    ┘
```

**Oura path:**
```
Oura Readiness ┐
Oura Sleep     ├→ Combine Oura APIs → Transform Oura → Save Oura
Oura Activity  ┘
```

This approach uses n8n's built-in Merge node to properly combine the inputs, then the Code node just transforms the merged data.

## Why This Works

1. **Merge node** waits for all 3 inputs and combines them
2. **Code node** receives a single execution with all data
3. **$input.all()** now returns all 3 API responses
4. We can safely access each response

Try this and the workflow should execute properly!
