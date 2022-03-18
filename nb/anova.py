
import pandas as pd
import pingouin as pg




def run_anova():

    df = pd.read_csv("demo-math.csv")
    df.drop(df.columns[0], axis=1, inplace=True)
    print("data loaded...")
    factors = ["black_1", "english_language_learners_1", "students_with_disabilities_1", "poverty_1"]
    print("running anova")
    aov = pg.anova(dv='mean_scale_score', between=factors, data=df, detailed=True)
    print(aov)

run_anova()
