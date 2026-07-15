from flask import Flask, render_template, request, send_file, session

import pandas as pd

from datetime import datetime


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)


from reportlab.lib import colors

from reportlab.lib.pagesizes import letter


from src.predict import predict_country





app = Flask(__name__)


# Session key
app.secret_key = "hdi_prediction_secret_key"







# ==========================================
# LOAD DATASET
# ==========================================


df = pd.read_csv(

    "dataset/HDI.csv"

)



countries = sorted(

    df["Country"].unique()

)



MODEL_ACCURACY = 96.8







# ==========================================
# COUNTRY FLAGS
# ==========================================


country_flags = {


    "Germany":"🇩🇪",

    "India":"🇮🇳",

    "United States":"🇺🇸",

    "United Kingdom":"🇬🇧",

    "France":"🇫🇷",

    "Japan":"🇯🇵",

    "China":"🇨🇳",

    "Canada":"🇨🇦",

    "Australia":"🇦🇺"

}









# ==========================================
# HOME
# ==========================================


@app.route("/")
def home():


    return render_template(

        "home.html"

    )









# ==========================================
# PREDICTION PAGE
# ==========================================


@app.route("/predict")
def predict():


    return render_template(

        "indexnew.html",

        countries=countries

    )









# ==========================================
# RESULT
# ==========================================


@app.route("/result", methods=["POST"])
def result():


    country = request.form.get(

        "country"

    )




    if not country:


        return "Please Select a Country"






    data = predict_country(

        country

    )




    if data is None:


        return "Country Not Found"






    prediction = float(

        data["prediction"]

    )




    score = round(

        prediction * 100,

        2

    )









    if prediction >= 0.800:


        level = "Very High Human Development"

        color = "#00b894"



        recommendation = (

            "Excellent human development level.\n\n"

            "- Maintain strong healthcare systems.\n\n"

            "- Continue investment in quality education.\n\n"

            "- Support sustainable economic growth."

        )







    elif prediction >= 0.700:



        level = "High Human Development"

        color = "#0984e3"



        recommendation = (

            "Good development level.\n\n"

            "- Improve education quality.\n\n"

            "- Strengthen healthcare facilities.\n\n"

            "- Create more employment opportunities."

        )








    elif prediction >= 0.550:



        level = "Medium Human Development"

        color = "#fdcb6e"



        recommendation = (

            "Average development level.\n\n"

            "- Increase education accessibility.\n\n"

            "- Improve healthcare infrastructure.\n\n"

            "- Focus on income and employment growth."

        )








    else:



        level = "Low Human Development"

        color = "#d63031"



        recommendation = (

            "Development improvement required.\n\n"

            "- Provide better healthcare facilities.\n\n"

            "- Improve basic education access.\n\n"

            "- Develop economic opportunities."

        )







    flag = country_flags.get(

        country,

        "🌍"

    )







    generated_time = datetime.now().strftime(

        "%d %B %Y | %I:%M %p"

    )







    # SAVE DATA FOR PDF


    report_data = {


        "country": country,


        "prediction": round(

            prediction,

            3

        ),


        "score": score,


        "level": level,


        "recommendation": recommendation,


        "generated": generated_time


    }




    session["prediction_report"] = report_data







    return render_template(


        "resultnew.html",


        prediction=round(

            prediction,

            3

        ),


        score=score,


        level=level,


        color=color,


        recommendation=recommendation,


        data=data,


        flag=flag,


        generated_time=generated_time


    )
# ==========================================
# DOWNLOAD PDF REPORT
# ==========================================


@app.route("/download_report")
def download_report():


    prediction_report = session.get(

        "prediction_report",

        {}

    )



    pdf_file = "HDI_Prediction_Report.pdf"




    doc = SimpleDocTemplate(

        pdf_file,

        pagesize=letter

    )




    styles = getSampleStyleSheet()




    title_style = ParagraphStyle(

        "title",

        parent=styles["Title"],

        alignment=1,

        textColor=colors.HexColor("#0f766e"),

        fontSize=22

    )





    heading_style = ParagraphStyle(

        "heading",

        parent=styles["Heading2"],

        textColor=colors.HexColor("#0f766e")

    )






    content = []







    # TITLE


    content.append(

        Paragraph(

            "Human Development Index Prediction Report",

            title_style

        )

    )




    content.append(

        Spacer(1,20)

    )








    # REPORT PURPOSE


    content.append(

        Paragraph(

            "Report Purpose",

            heading_style

        )

    )





    content.append(

        Paragraph(

            "This report contains the Human Development Index "
            "prediction generated by the Machine Learning based "
            "HDI Prediction System. It is useful for analysis, "
            "documentation and future reference.",

            styles["BodyText"]

        )

    )






    content.append(

        Spacer(1,25)

    )







    if prediction_report:




        content.append(

            Paragraph(

                "Prediction Details",

                heading_style

            )

        )







        details = [


            [

                "Country",

                prediction_report["country"]

            ],



            [

                "Predicted HDI",

                str(prediction_report["prediction"])

            ],



            [

                "HDI Score",

                str(prediction_report["score"]) + "%"

            ],



            [

                "Development Level",

                prediction_report["level"]

            ],



            [

                "Generated Time",

                prediction_report["generated"]

            ]



        ]







        table = Table(

            details,

            colWidths=[160,250]

        )







        table.setStyle(

            TableStyle([



                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.grey

                ),



                (

                    "BACKGROUND",

                    (0,0),

                    (0,-1),

                    colors.HexColor("#ccfbf1")

                ),



                (

                    "PADDING",

                    (0,0),

                    (-1,-1),

                    10

                )



            ])

        )






        content.append(table)







        content.append(

            Spacer(1,25)

        )







        # RECOMMENDATION


        content.append(

            Paragraph(

                "Recommendation",

                heading_style

            )

        )







        content.append(

            Paragraph(

                prediction_report["recommendation"].replace(

                    "\n\n",

                    "<br/><br/>"

                ),

                styles["BodyText"]

            )

        )







        content.append(

            Spacer(1,25)

        )








        # MODEL DETAILS


        content.append(

            Paragraph(

                "Model Information",

                heading_style

            )

        )







        model_table = Table(


            [

                [

                    "Algorithm",

                    "Linear Regression"

                ],



                [

                    "Model Accuracy",

                    str(MODEL_ACCURACY) + "%"

                ]

            ],


            colWidths=[160,250]

        )








        model_table.setStyle(

            TableStyle([



                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    1,

                    colors.grey

                ),



                (

                    "PADDING",

                    (0,0),

                    (-1,-1),

                    10

                )



            ])

        )







        content.append(

            model_table

        )







    else:



        content.append(

            Paragraph(

                "No prediction data available.",

                styles["BodyText"]

            )

        )








    doc.build(

        content

    )







    return send_file(

        pdf_file,

        as_attachment=True

    )
# ==========================================
# DASHBOARD
# ==========================================


@app.route("/dashboard")
def dashboard():



    total = len(df)




    avg = round(

        df["HDI"].mean(),

        3

    )







    highest = df.loc[

        df["HDI"].idxmax(),

        "Country"

    ]







    lowest = df.loc[

        df["HDI"].idxmin(),

        "Country"

    ]








    current_time = datetime.now().strftime(

        "%d %B %Y | %I:%M %p"

    )








    return render_template(

        "dashboard.html",

        total=total,

        avg=avg,

        highest=highest,

        lowest=lowest,

        accuracy=MODEL_ACCURACY,

        current_time=current_time

    )









# ==========================================
# ABOUT
# ==========================================


@app.route("/about")
def about():


    return render_template(

        "about.html"

    )









# ==========================================
# RUN APPLICATION
# ==========================================


if __name__ == "__main__":


    app.run(

        debug=True

    )