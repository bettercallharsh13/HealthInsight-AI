import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
@dataclass
class User:
    name: str
    age: int
    height: float  # cm
    weight: float  # kg
    sleep: float   # hours
    water: float   # liters
    id: Optional[int] = None

    def __post_init__(self):
        """Validate data after initialization"""
        if self.age <= 0 or self.age > 120:
            raise ValueError("Age must be between 1 and 120")
        if self.weight <= 0 or self.weight > 300:
            raise ValueError("Weight must be between 1 and 300 kg")
        if self.height <= 0 or self.height > 250:
            raise ValueError("Height must be between 1 and 250 cm")
        if self.water < 0 or self.water > 10:
            raise ValueError("Water consumption should be between 0 and 10L")
        if self.sleep < 0 or self.sleep > 24:
            raise ValueError("Sleep hours must be between 0 and 24")


class HealthAnalyzer:
    def __init__(self, user):
        self.user = user

    def bmi(self) -> float:
        return self.user.weight / ((self.user.height / 100) ** 2)

    def bmi_status(self) -> str:

        bmi = self.bmi()

        if bmi < 18.5:
            return "Under weight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Over weight"
        else:
            return "Obese"

    def health_score(self) -> int:

        score = 100

        bmi = self.bmi()

        if bmi < 18.5:
            score -= (18.5 - bmi) * 2

        elif bmi > 25:
            score -= (bmi - 25) * 2

        if self.user.sleep < 7:
            score -= (7 - self.user.sleep) * 3

        if self.user.water < 2:
            score -= (2 - self.user.water) * 5

        return max(0, min(100, score))

    def recommendations(self) -> List[str]:

        tip = []

        if self.bmi() > 25:
            tip.append("Increase physical activity.")

        elif self.bmi() < 18.5:
            tip.append("Increase calories intake through balanced meals.")

        if self.user.sleep < 7:
            tip.append("Sleep at least 7-9 hours.")

        if self.user.water < 2:
            tip.append("Drink more water")

        return tip or ["No major concerns. Maintain healthy habits!"]

    def ai_insight(self) -> str:

        insights = [f"{self.user.name} has a BMI of {self.bmi():.1f}."]

        if self.bmi() < 18.5:
            insights.append("Consider gaining weight through a balanced diet.")
        elif self.bmi() > 25:
            insights.append("Consider weight management through diet and exercise.")
        else:
            insights.append("Your BMI is in the healthy range.")

        if self.user.sleep < 7:
            insights.append(f"Sleep {7 - self.user.sleep:.1f} more hours per night.")
        elif self.user.sleep > 9:
            insights.append("You may be sleeping too much.")

        if self.user.water < 2:
            insights.append(f"Drink {2 - self.user.water:.1f}L more water daily.")

        return " ".join(insights)


    def get_trend_analysis(self, history: List[Dict]) -> Dict:

            if not history:
                return {"trend": "Insufficient data"}

            recent = history[-5:]  # Last 5 records
            scores = [h.get('score', 0) for h in recent]

            if len(scores) > 1:
                trend = "improving"
                if scores[-1] > scores[0]:
                    trend ="improving"
                elif scores[-1] < scores[0]:
                    trend = "declining"
                else:
                    trend ="stable"

                return {
                    "trend": trend,
                    "current_score": scores[-1],
                    "change": scores[-1] - scores[0],
                    "records_analyzed": len(scores)
                }
            return {"trend": "stable", "records_analyzed": len(scores)}

def save_report(data):
    try:
        with open("history.json", "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):

        history = []

    history.append(data)

    with open("history.json", "w") as file:
        json.dump(history, file, indent=2)

def get_positive_float(promt: str, max_value: Optional[float] = None) -> float:
    while True:
        try:
            value = float(input(promt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            if max_value and value > max_value:
                print(f"Please enter a value less than {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number")

def get_positive_int(prompt: str, max_value: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            if max_value and value > max_value:
                print(f"Please enter a value less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")



def main():
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age = get_positive_int("Age: ", max_value=120)
    weight = get_positive_float("Weight (in kg): ", max_value=300)
    height = get_positive_float("Height (in cm): ", max_value=250)
    sleep = get_positive_float("Sleeping Hours: ", max_value=24)
    water = get_positive_float("Daily Water Consumption (in liter) : ", max_value=10)

    user = User(
            name,
            age,
            weight,
            height,
            sleep,
            water
    )

    analyzer = HealthAnalyzer(user)

    report = {
        "date": str(datetime.now()),
        "name": user.name,
        "bmi": round(analyzer.bmi(), 2),
        "status": analyzer.bmi_status(),
        "score": analyzer.health_score()
    }

    save_report(report)

    print("\n===== HEALTH REPORT =====")
    print(f"BMI: {analyzer.bmi():.2f}")
    print(f"Status: {analyzer.bmi_status()}")
    print(f"Health Score: {analyzer.health_score()}/100")

    print("\nRecommendations:")
    for tip in analyzer.recommendations():
        print("-", tip)

    print("\nAI Insight:")
    print(analyzer.ai_insight())
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
        trend = analyzer.get_trend_analysis(history)
        if trend.get('records_analyzed', 0) > 1:
            print(f"\n📈 Trend: {trend['trend']} (Score: {trend['current_score']})")
            if trend.get('change', 0) != 0:
                print(f"    change: {trend['change']:+d} points")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    print("="*50)


if __name__ == "__main__":
    main()
