print("PROGRAM STARTED_363")
import random
import time


def Linear_Search_363(Data_363, Target_363):
    for Index_363 in range(len(Data_363)):
        if Data_363[Index_363] == Target_363:
            return Index_363
    return -1


def Binary_Search_363(Data_363, Target_363):
    Low_363 = 0
    High_363 = len(Data_363) - 1

    while Low_363 <= High_363:
        Mid_363 = (Low_363 + High_363) // 2

        if Data_363[Mid_363] == Target_363:
            return Mid_363

        elif Data_363[Mid_363] < Target_363:
            Low_363 = Mid_363 + 1

        else:
            High_363 = Mid_363 - 1

    return -1


def Generate_Data_363(Size_363):
    Data_363 = random.sample(range(1, Size_363 * 10 + 1), Size_363)
    return Data_363


def Measure_Time_363(Search_Function_363, Data_363, Target_363, Repetitions_363):
    Start_Time_363 = time.perf_counter()

    for Count_363 in range(Repetitions_363):
        Search_Function_363(Data_363, Target_363)

    End_Time_363 = time.perf_counter()

    Total_Time_363 = End_Time_363 - Start_Time_363
    Average_Time_363 = Total_Time_363 / Repetitions_363

    return Average_Time_363


def Main_363():
    Input_Sizes_363 = [
        1000,
        5000,
        10000,
        50000,
        100000,
        500000,
        1000000
    ]

    Repetitions_363 = 10

    print("=" * 80)
    print("LINEAR SEARCH VS BINARY SEARCH PERFORMANCE")
    print("=" * 80)

    print(
        f"{'Input Size':>15}"
        f"{'Linear Search (s)':>25}"
        f"{'Binary Search (s)':>25}"
    )

    print("-" * 80)

    for Size_363 in Input_Sizes_363:

        # Generate random dataset
        Data_363 = Generate_Data_363(Size_363)

        # Select an element that is guaranteed to exist
        Target_363 = Data_363[-1]

        # Measure Linear Search
        Linear_Time_363 = Measure_Time_363(
            Linear_Search_363,
            Data_363,
            Target_363,
            Repetitions_363
        )

        # Sort dataset before Binary Search
        Sorted_Data_363 = sorted(Data_363)

        # Measure Binary Search
        Binary_Time_363 = Measure_Time_363(
            Binary_Search_363,
            Sorted_Data_363,
            Target_363,
            Repetitions_363
        )

        print(
            f"{Size_363:>15,}"
            f"{Linear_Time_363:>25.10f}"
            f"{Binary_Time_363:>25.10f}"
        )

    print("=" * 80)


if __name__ == "__main__":
    Main_363()