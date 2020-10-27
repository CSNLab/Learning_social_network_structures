var norbeck_social_support_json = {
 locale: "en",
 pages: [],  // filled in later
 showCompletedPage: false,
 showPageTitles: false,
 showPrevButton: false,
 showQuestionNumbers: "off",
 showTitle: false,
 title: "Norbeck Social Support"
};

var norbeck_social_support_page = {
 name: "page",
 elements: [
  {
   type: "matrix",
   isAllRowRequired: true,
   name: "question1",
   title: "Please answer the questions below for: ",
   columns: [
    {
     value: "0",
     text: "Not at all"
    },
    {
     value: "1",
     text: "A little"
    },
    {
     value: "2",
     text: "Moderately"
    },
    {
     value: "3",
     text: "Quite a bit"
    },
    {
     value: "4",
     text: "A great deal"
    }
   ],
   rows: [
    {
     value: "1",
     text: "How much has this person made you feel loved or liked?"
    },
    {
     value: "2",
     text: "How much has this person made you feel admired or respected?"
    },
    {
     value: "3",
     text: "How much can you confide in this person?"
    },
    {
     value: "4",
     text: "How much does this person agree with or support your thought?"
    },
    {
     value: "6",
     text: "How much would this person help if you needed to borrow money, or a ride to a hospital or any other help?"
    },
    {
     value: "7",
     text: "If you were hospitalized and confined to bed, how much could this person help you?"
    }
   ]
  },
  {
   type: "radiogroup",
   choices: [
    {
     value: "1",
     text: "less than 6 months"
    },
    {
     value: "2",
     text: "6-12 months"
    },
    {
     value: "3",
     text: "1-2 years"
    },
    {
     value: "4",
     text: "2-5 years"
    },
    {
     value: "5",
     text: "more than 5 years"
    }
   ],
   isRequired: true,
   name: "question2",
   title: "How long have you known this person?"
  },
  {
   type: "radiogroup",
   choices: [
    {
     value: "1",
     text: "once a year or less"
    },
    {
     value: "2",
     text: "a few times in a year"
    },
    {
     value: "3",
     text: "monthly"
    },
    {
     value: "4",
     text: "weekly"
    },
    {
     value: "5",
     text: "daily"
    }
   ],
   isRequired: true,
   name: "question3",
   title: "How frequently do you contact this person?"
  },
  {
   type: "radiogroup",
   choices: [
    {
     value: "1",
     text: "A little close or not close"
    },
    {
     value: "2",
     text: "Somewhat close"
    },
    {
     value: "3",
     text: "Very close"
    }
   ],
   name: "question4",
   isRequired: true,
   title: "How close do you feel to this person?"
  },
  {
   type: "radiogroup",
   choices: [
    {
     value: "1",
     text: "At the same address"
    },
    {
     value: "2",
     text: "Within walking distance (but not at the same address)"
    },
    {
     value: "3",
     text: "10 minutes to 1 hour's drive away"
    },
    {
     value: "4",
     text: "1-3 hours' drive away"
    },
    {
     value: "5",
     text: "3-10 hours' drive away (or under a 2-hour flight)"
    },
    {
     value: "6",
     text: "Outside driving distance but in the same country and continent"
    },
    {
     value: "7",
     text: "In a different country or continent"
    }
   ],
   name: "question5",
   isRequired: true,
   title: "How close does this person live to you?"
  }
 ]
};
