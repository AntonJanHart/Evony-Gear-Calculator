#!/usr/bin/env python3
import sys
import argparse

def calculate_units_needed(target_level, current_units):
    """
    Calculate exactly how many units need to be purchased to reach the target level.
    
    Args:
        target_level (int): The desired level to reach (1-indexed)
        current_units (list): List of current units at each level, starting from level 1

        Example:
            # To reach level 7 with units at levels 1-6
            python level_calculator.py 1,0,1,2,1,2

            # Using spaces instead of commas
            python level_calculator.py 1 0 1 2 1 2
    
    Returns:
        tuple: (units_to_buy, total_cost, final_units)
    """
    UNIT_COST = 200

    # If we already have at least one unit at the target level, we're done
    if len(current_units) >= target_level and current_units[target_level-1] > 0:
        return 0, 0, current_units
    
    # Calculate the total equivalent level 1 units based on what we have
    total_equivalent_units = 0
    for level, count in enumerate(current_units):
        # Each unit at level N is worth 3^(N-1) units at level 1
        total_equivalent_units += count * (3 ** level)
    
    # Calculate how many level 1 units are needed for one unit at the target level
    units_needed_for_target = 3 ** (target_level - 1)
    
    # Calculate how many more level 1 units to buy
    units_to_buy = max(0, units_needed_for_target - total_equivalent_units)
    total_cost = units_to_buy * UNIT_COST
    
    # Calculate final distribution of units
    # At target level we'll have exactly 1 unit
    final_units = [0] * target_level
    final_units[target_level-1] = 1
    
    # Calculate remaining units after conversion
    # First, how many level 1 equivalent units we'll have total
    total_units = total_equivalent_units + units_to_buy
    
    # The remaining units after creating the target level unit
    remaining = total_units - units_needed_for_target
    
    # Distribute remaining units from bottom to top
    for level in range(target_level - 1):
        # How many units remain at this level
        final_units[level] = remaining % (3 ** (level + 1)) // (3 ** level)
        
    return units_to_buy, total_cost, final_units

def format_units_output(units):
    """Format units with level names for display"""
    result = []
    for i, count in enumerate(units):
        result.append(f"Lv{i+1}: {count}")
    return ", ".join(result)

def main():
    parser = argparse.ArgumentParser(description='Calculate units needed to reach the next level.')
    parser.add_argument('units', type=str, nargs='+', help='Current units at each level')
    
    args = parser.parse_args()
    
    # Parse current units
    current_units = []
    for unit in args.units:
        # Handle comma-separated values
        if ',' in unit:
            for val in unit.split(','):
                if val.strip():  # Skip empty values
                    current_units.append(int(val.strip()))
        else:
            current_units.append(int(unit))
    
    # Target level is the next level after the last one provided
    target_level = len(current_units) + 1
    
    units_to_buy, total_cost, final_units = calculate_units_needed(target_level, current_units)
    
    print(f"Target Level: {target_level}")
    print(f"Units to buy: {units_to_buy}")
    print(f"Total Gems: {total_cost:,}")
    print(f"Final units distribution: {format_units_output(final_units)}")

if __name__ == "__main__":
    main()