import pandas as pd

import numpy as np

if __name__ == '__main__':

    df = pd.read_csv("data/BC - AI ORIGINAL.csv", delimiter=',')

    YELLOW_NUM = 17

    GREEN_NUM = 6

    BLUE_NUM = 19

    # print(df[:5])

    first_form = df['MJIL 1000 08 10']

    liquor_col = df['Liquor Liability']

    emp_ben_col = df['Employee Benefits Liability']

    # df2 = [first_form, liquor_col, emp_ben_col]

    # df2 = first_form.merge(liquor_col).merge(emp_ben_col)

    df2 = pd.DataFrame(np.array([first_form, liquor_col, emp_ben_col])).T

    print(df2[:5])

    df2 = df2.rename(columns={0:'Form', 1: "Liq", 2: "Emp"})

    print("Columns")
    print(df2.columns)

    # print(df2['Form'].count())
    # print(df2[df2['Form'] == 1].count())

    have_form = df2[df2['Form'] == 1]

    have_liq = have_form[have_form['Liq'] == 1]['Liq'].count()
    
    print(f"Have liq: {have_liq}")

    dont_have_liq = have_form[have_form['Liq'] == 0]['Liq'].count()

    print(f"Don't have liq: {dont_have_liq}")


    have_Emp = have_form[have_form['Emp'] == 1]['Emp'].count()
    
    print(f"Have Emp: {have_Emp}")

    dont_have_Emp = have_form[have_form['Emp'] == 0]['Emp'].count()

    print(f"Don't have Emp: {dont_have_Emp}")

    # print()