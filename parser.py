import re
from datetime import datetime
from typing import Self, override


class BloodPressure:
    def __init__(self, systolic: int, diastolic: int, dt: datetime, is_h: bool):
        self.systolic: float = float(systolic)
        self.diastolic: float = float(diastolic)
        self.dt: datetime = dt
        self.weight: float = 1.0 if not is_h else 0.5

    def combine(self, other: Self):
        self.systolic = (
            self.systolic * self.weight + other.systolic * other.weight
        ) / (self.weight + other.weight)
        self.diastolic = (
            self.diastolic * self.weight + other.diastolic * other.weight
        ) / (self.weight + other.weight)
        self.weight = self.weight + other.weight

    @override
    def __str__(self) -> str:
        return f"{self.dt} {int(self.systolic)}/{int(self.diastolic)}"

    def is_evening(self) -> bool:
        if self.dt.hour < 15:
            return False
        else:
            return True

    def dt_sub(self, other: Self) -> int:
        dt_sub: int = int((self.dt - other.dt).total_seconds())
        assert dt_sub >= 0
        return dt_sub


bp_list: list[BloodPressure] = []

with open("data.txt", "r") as f:
    for line in f.readlines():
        reg = r"^(\d+)\/(\d+)\s(\d+)[\:\.](\d+)\s*\-\-\s*(\d+)\/(\d+)\s*(\(h\))?\s*$"
        match = re.search(reg, line)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = 24
            hour = match.group(3)
            minute = match.group(4)
            systolic = match.group(5)
            diastolic = match.group(6)
            is_h = match.group(7) is not None
            dt = datetime.strptime(
                f"{day}/{month}/{year} {hour}:{minute}", r"%d/%m/%y %H:%M"
            )
            bp = BloodPressure(
                systolic=int(systolic), diastolic=int(diastolic), dt=dt, is_h=is_h
            )
            if len(bp_list) > 0:
                last_bp = bp_list[len(bp_list) - 1]
                if bp.dt_sub(last_bp) <= 60 * 30:
                    last_bp.combine(bp)
                    continue
            bp_list.append(bp)

# print(len(bp_list))

with open("afternoon.txt", "w") as f:
    f.write("AFTERNOON\n")
    for bp in bp_list:
        if not bp.is_evening():
            # f.write(f"{bp} {bp.weight}\n")
            f.write(f"{bp}\n")

with open("evening.txt", "w") as f:
    f.write("EVENING\n")
    for bp in bp_list:
        if bp.is_evening():
            # f.write(f"{bp} {bp.weight}\n")
            f.write(f"{bp}\n")
