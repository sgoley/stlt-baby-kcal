import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Baby Kcal Calculator")

st.sidebar.title("Inputs 🔢")

# Input fields for baby's nutrition calculations
current_weight = st.sidebar.number_input(
    "Baby's Current Weight (kg)",
    min_value=0.0,
    max_value=30.0,
    value=4.000,  # Default value based on the data showing ~4kg
    step=0.001,
    help="Enter baby's current weight in kg"
)

target_calories = st.sidebar.number_input(
    "Target Calories per kg",
    min_value=0,
    max_value=200,
    value=120,  # Common target for infants
    step=1,
    help="Enter target calories per kg of body weight"
)

feed_calories_per_ounce = st.sidebar.number_input(
    "Feed Calories per 1oz",
    min_value=0,
    max_value=100,
    value=20,
    step=1,
    help="Enter calories per 1oz of formula"
)

feeding_size = st.sidebar.number_input(
    "Feeding Size (ml)",
    min_value=1,
    max_value=2000,
    value=100,  # Common feeding frequency
    step=1,
    help="Enter number of feedings per day"
)

formula_kcal = st.sidebar.number_input(
    "Formula Calories per tsp",
    min_value=0,
    max_value=10,
    value=2.5,  # Standard formula calories
    step=0.1,
    help="Enter calories per tsp of formula"
)

# Main display panel
st.header("📊 Nutrition Calculations")

# Calculate total daily calories goal
total_daily_calories = current_weight * target_calories

# Convert feeding size from ml to oz (1 oz = 29.5735 ml)
feeding_size_oz = feeding_size / 29.5735

# Calculate calories per feeding
calories_per_feeding = feed_calories_per_ounce * feeding_size_oz

# Calculate feedings per day
if calories_per_feeding > 0:
    feedings_per_day = total_daily_calories / calories_per_feeding
else:
    feedings_per_day = 0

# Display results in columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Daily Calories Goal",
        value=f"{total_daily_calories:.1f} kcal",
        help="Target calories per kg × current weight"
    )

with col2:
    st.metric(
        label="Feedings Per Day",
        value=f"{feedings_per_day:.1f}",
        help="Total daily calories ÷ calories per feeding"
    )

st.divider()


# Additional helpful information
st.subheader("📋 Feeding Schedule Breakdown")

# Create a more detailed breakdown
col3, col4, col5, col6 = st.columns(4)

with col3:
    if feedings_per_day > 0:
        hours_between_feedings = 24 / feedings_per_day
        hours = int(hours_between_feedings)
        minutes = int((hours_between_feedings - hours) * 60)
        st.info(f"**Hours Between Feedings:** {hours}h {minutes}m")
    else:
        st.info("**Hours Between Feedings:** N/A")

with col4:
    st.info(f"**Feeding Size:** {feeding_size} ml ({feeding_size_oz:.1f} oz)")

with col5:
    st.info(f"**Calories per Feeding:** {calories_per_feeding:.1f} kcal")

with col6:
    # Calculate formula powder addition needed
    # Standard formula: 67 kcal per 100ml = 19.8 kcal per oz (67 * 29.5735/100)
    standard_kcal_per_oz = (formula_kcal * 29.5735) / 100
    
    if feed_calories_per_ounce > standard_kcal_per_oz:
        # Calculate extra calories needed per oz
        extra_kcal_needed = feed_calories_per_ounce - standard_kcal_per_oz
        
        # Assuming 1 tsp of formula powder adds approximately 2.5 kcal per oz
        # This is a typical approximation - may vary by formula brand
        kcal_per_tsp = 2.5
        tsp_needed = extra_kcal_needed / kcal_per_tsp
        
        # Convert to fractions for easier measurement
        if tsp_needed < 0.125:
            powder_instruction = "No extra powder needed"
        elif tsp_needed < 0.25:
            powder_instruction = "~1/8 tsp per oz"
        elif tsp_needed < 0.375:
            powder_instruction = "~1/4 tsp per oz"
        elif tsp_needed < 0.625:
            powder_instruction = "~1/2 tsp per oz"
        elif tsp_needed < 0.875:
            powder_instruction = "~3/4 tsp per oz"
        else:
            powder_instruction = f"~{tsp_needed:.1f} tsp per oz"
        
        st.info(f"**Extra Powder:** {powder_instruction}")
    else:
        st.info(f"**Extra Powder:** None needed")

# Add expandable information section
with st.expander("🥄 Formula Powder Calculator - How it Works"):
    st.markdown("""
    ### How it works:
    1. **Calculates standard calories per oz** from your formula ({:.1f} kcal/100ml = ~{:.1f} kcal/oz)
    2. **Compares to your target** (e.g., {} kcal/oz)
    3. **Calculates extra powder needed** using the approximation that 1 tsp adds ~2.5 kcal/oz
    4. **Converts to practical fractions** for easy measuring
    
    ### Example outputs:
    - **If you want 22 kcal/oz** and standard is 19.8 kcal/oz:
      - Extra needed: 2.2 kcal/oz
      - Result: **"~1/4 tsp per oz"**
    
    - **If you want 24 kcal/oz**:
      - Extra needed: 4.2 kcal/oz  
      - Result: **"~1/2 tsp per oz"**
    
    ### Important Notes:
    - The 2.5 kcal per teaspoon approximation may vary by formula brand
    - Always consult your pediatrician before modifying formula concentrations
    - Measure powder carefully for consistent results
    """.format(formula_kcal, standard_kcal_per_oz, feed_calories_per_ounce))

# Warning if calculations seem unusual
if feedings_per_day > 20:
    st.warning("⚠️ More than 20 feedings per day seems unusually high. Please check your inputs.")
elif feedings_per_day < 4:
    st.warning("⚠️ Fewer than 4 feedings per day seems unusually low for an infant. Please check your inputs.")

st.divider()

# Feeding Tracker Section
st.header("🍼 Today's Feeding Tracker")

# Initialize session state for feeding data
if 'feeding_data' not in st.session_state:
    st.session_state.feeding_data = pd.DataFrame({
        'Time': ['1:00 AM', '4:00 AM', '7:00 AM', '9:00 AM'],
        'Amount (ml)': [60, 75, 60, 30],
        'Completed': [True, True, True, True]
    })

# Create editable table
st.subheader("📝 Enter Today's Feeds")
edited_data = st.data_editor(
    st.session_state.feeding_data,
    column_config={
        "Time": st.column_config.TextColumn(
            "Time",
            help="Enter feeding time (e.g., '1:00 AM', '14:30')",
            max_chars=10,
        ),
        "Amount (ml)": st.column_config.NumberColumn(
            "Amount (ml)",
            help="Amount fed in milliliters",
            min_value=0,
            max_value=500,
            step=5,
        ),
        "Completed": st.column_config.CheckboxColumn(
            "Completed",
            help="Check if this feeding has been completed",
            default=False,
        )
    },
    num_rows="dynamic",
    use_container_width=True,
    key="feeding_editor"
)

# Update session state
st.session_state.feeding_data = edited_data

# Calculate feeding progress
completed_feeds = edited_data[edited_data['Completed'] == True]
total_consumed_ml = completed_feeds['Amount (ml)'].sum()

# Calculate calories consumed
calories_consumed = (total_consumed_ml / 100) * formula_kcal

# Calculate remaining needs
remaining_calories = total_daily_calories - calories_consumed
remaining_ml = (remaining_calories / formula_kcal) * 100

# Display progress
st.subheader("📊 Today's Progress")

progress_col1, progress_col2, progress_col3 = st.columns(3)

with progress_col1:
    st.metric(
        label="Consumed Today",
        value=f"{total_consumed_ml:.0f} ml",
        delta=f"{calories_consumed:.0f} kcal"
    )

with progress_col2:
    st.metric(
        label="Remaining Needed",
        value=f"{remaining_ml:.0f} ml",
        delta=f"{remaining_calories:.0f} kcal"
    )

with progress_col3:
    progress_percentage = min((calories_consumed / total_daily_calories) * 100, 100)
    st.metric(
        label="Daily Goal Progress",
        value=f"{progress_percentage:.1f}%"
    )

# Generate remaining feeding schedule
if remaining_calories > 0:
    st.subheader("🕐 Suggested Remaining Schedule")
    
    # Calculate how many more feeds needed
    remaining_feeds_needed = remaining_calories / calories_per_feeding
    
    # Find the most recent completed feed time
    def parse_time_string(time_str):
        """Parse time string to datetime object for today"""
        try:
            # Handle different time formats
            time_str = time_str.strip().upper()
            
            # Try parsing with AM/PM first
            for fmt in ['%I:%M %p', '%I %p', '%H:%M']:
                try:
                    parsed_time = datetime.strptime(time_str, fmt)
                    # Set to today's date
                    today = datetime.now().date()
                    return datetime.combine(today, parsed_time.time())
                except ValueError:
                    continue
            
            # If no format worked, return None
            return None
        except:
            return None
    
    # Get the latest completed feed time
    latest_feed_time = None
    if not completed_feeds.empty:
        completed_times = []
        for time_str in completed_feeds['Time']:
            parsed_time = parse_time_string(str(time_str))
            if parsed_time:
                completed_times.append(parsed_time)
        
        if completed_times:
            latest_feed_time = max(completed_times)
    
    # Determine start time for next feeds
    now = datetime.now()
    if latest_feed_time and latest_feed_time > now:
        # If latest feed is in the future, start from that time + minimum interval
        start_time = latest_feed_time + timedelta(hours=1)  # Minimum 1 hour gap
    else:
        # Start from current time or 1 hour after latest feed, whichever is later
        min_next_time = now
        if latest_feed_time:
            min_next_time = max(now, latest_feed_time + timedelta(hours=1))
        start_time = min_next_time
    
    # Calculate feeding interval (assuming feeds until 11 PM)
    end_of_day = now.replace(hour=23, minute=0, second=0, microsecond=0)
    
    # If start time is after end of day, move to tomorrow
    if start_time.date() > now.date():
        end_of_day = end_of_day + timedelta(days=1)
    
    hours_remaining = (end_of_day - start_time).total_seconds() / 3600
    
    if hours_remaining > 0 and remaining_feeds_needed > 0:
        interval_hours = max(1.5, hours_remaining / remaining_feeds_needed)  # Minimum 1.5 hour intervals
        
        # Generate suggested schedule
        suggested_schedule = []
        current_time = start_time
        
        for i in range(int(remaining_feeds_needed) + 1):
            if current_time <= end_of_day:
                suggested_schedule.append({
                    'Suggested Time': current_time.strftime('%I:%M %p'),
                    'Amount (ml)': feeding_size,
                    'Calories': calories_per_feeding
                })
                current_time += timedelta(hours=interval_hours)
        
        if suggested_schedule:
            schedule_df = pd.DataFrame(suggested_schedule)
            st.dataframe(schedule_df, use_container_width=True)
            
            latest_time_str = latest_feed_time.strftime('%I:%M %p') if latest_feed_time else "now"
            st.info(f"💡 **Recommendation:** Starting from after {latest_time_str}, feed approximately every {interval_hours:.1f} hours with {feeding_size} ml per feeding to meet daily goal.")
        else:
            st.warning("⚠️ Not enough time remaining today to complete feeding goal. Consider extending feeding schedule or adjusting amounts.")
    else:
        if hours_remaining <= 0:
            st.warning("⚠️ Not enough time remaining today to complete feeding goal.")
        else:
            st.success("🎉 Daily calorie goal has been met!")
else:
    st.success("🎉 Daily calorie goal has been exceeded!")

# Progress bar
st.subheader("📈 Daily Progress Bar")
progress_bar_value = min(calories_consumed / total_daily_calories, 1.0)
st.progress(progress_bar_value)
st.caption(f"Progress: {calories_consumed:.0f} / {total_daily_calories:.0f} kcal")
