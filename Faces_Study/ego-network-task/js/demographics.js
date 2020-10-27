var demographics_json = {
 locale: "en",
 showCompletedPage: false,
 showPageTitles: false,
 showPrevButton: false,
 showQuestionNumbers: "off",
 showTitle: false,
 title: "Demographics",
 pages: [
  {
   name: "page1",
   elements: [
    {
     type: "text",
     name: "age",
     title: "Please enter your age",
     isRequired: true,
     inputType: "number"
    },
    {
     type: "dropdown",
     name: "gender",
     title: "Please select you gender",
     isRequired: true,
     hasOther: true,
     choices: [
      {
       value: "female",
       text: "Female"
      },
      {
       value: "male",
       text: "Male"
      },
      {
       value: "na",
       text: "Prefer not to answer"
      }
     ],
     otherText: "Other (describe)"
    },
    {
     type: "dropdown",
     name: "race",
     title: "Please select your race",
     isRequired: true,
     hasOther: true,
     choices: [
      {
       value: "white",
       text: "White"
      },
      {
       value: "latino",
       text: "Latino or Hispanic"
      },
      {
       value: "african",
       text: "African"
      },
      {
       value: "eastasian",
       text: "East Asian"
      },
      {
       value: "southasian",
       text: "South or Southeast Asian"
      },
      {
       value: "pacific",
       text: "Native Hawaiian or Other Pacific Islander"
      },
      {
       value: "native",
       text: "American Indian or Alaska Native"
      },
      {
       value: "mideastern",
       text: "Middle Eastern or Central Asian"
      },
      {
       value: "na",
       text: "Prefer not to answer"
      }
     ],
     otherText: "Other or Mixed (describe)"
    },
    {
      type: "matrixdropdown",
      name: "ucla_time",
      title: "How long have you been at UCLA?",
      isRequired: true,
      showHeader: false,
      width: "40%",
      columns: [
        {
          name: "duration",
          title: " ",
          cellType: "text",
          inputType: "number",
          validators: [{ type: "numeric",
                         minValue: 1,
                         maxValue: 10000 }]
        },
        {
          name: "unit",
          title: " ",
          choices: ["day(s)", "week(s)", "month(s)", "year(s)"]
        }
      ],
      rows: [{ text: " ", value: "0" }]
    }
   ]
  }
 ]
}