var social_network_list_json = {
  "pages": [
    {
      "title": "Consider the people with whom you like to spend your time. Since you arrived at UCLA, who are the people with whom you socialize and/or discuss important matters?",
      "elements": [
        {
          "type": "html",
          "name": "instructions1",
          "html": '<h5>Please list their first names, gender, and your relationship to that person below. <span class="blue">List as many or as few people as you need.</span></h5>'
        },
        {
          "type": "matrixdynamic",
          "cellType": "text",
          "choices": [
            {
              "value": "female",
              "text": "Female"
            },
            {
              "value": "male",
              "text": "Male"
            },
            {
              "value": "other",
              "text": "Other"
            }
          ],
          "columns": [
            {
              "name": "name",
              "title": "Name",
              "cellType": "text",
              "isRequired": false
            },
            {
              "name": "gender",
              "title": "Gender",
              "cellType": "dropdown",
              "isRequired": false
            },
            {
              "name": "relationship",
              "title": "Relationship (e.g. family member, friend, spouse, professional contact, etc.)",
              "cellType": "text",
              "isRequired": false
            }
          ],
          "isRequired": true,
          "name": "social-list",
          "title": " ",
          "rowCount": 20,
          "validators": [
            {
              type: "networklistvalidator"
            }
          ]
        },
        {
          type: "html",
          name: "instructions2",
          html: '<div class="blue" align="right">Please use as many or as few rows as necessary.</div>'
        },
      ]
    }
  ],
  showCompletedPage: false,
  showPrevButton: false,
  showQuestionNumbers: "off",
  showTitle: false,
  title: "Social Network List"
};

var ego_centric_network_matrix_json = {
  "pages": [
    {
      "title": "Please indicate who also socializes and/or discusses important matters with whom by checking or unchecking the boxes below.",
      "elements": [
        {
          "type": "matrixdropdown",
          "columns": [],
          "rows": [],
          "name": "social-network",
          "title": "Click on the checkbox once to indicate two people socialize and/or discuss important matters, or twice to indicate they do not.",
          "isRequired": true
        }
      ]
    }
  ],
  showCompletedPage: false,
  showPrevButton: false,
  showQuestionNumbers: "off",
  showTitle: false,
  title: "Ego Centric Network Matrix"
};

var norbeck_q1_json = {
  "pages":[
    {
      "title": "Please answer the questions below.",
      "elements": [
        {
          "type": "matrix",
          "isAllRowRequired": true,
          "name": "social-network-frequency",
          "title": "How frequently do you contact this person?",
          "columns": [
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
          rows: [],
        }
      ]
    },
    {
      "title": "Please answer the questions below.",
      "elements": [
        {
          "type": "matrix",
          "isAllRowRequired": true,
          "name": "social-network-closeness",
          "title": "How close do you feel to this person?",
          "columns": [
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
          rows: [],
        }
      ]
    },
  ],
  showCompletedPage: false,
  showPrevButton: false,
  showQuestionNumbers: "off",
  showTitle: false,
  title: "Norbeck Q1"
};
