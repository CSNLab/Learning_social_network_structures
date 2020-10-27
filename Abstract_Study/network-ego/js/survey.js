'use strict';

function shuffleArray(array, min_index, max_index) {  // includes min, excludes max
    for (let i = max_index - 1; i > min_index; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}


(function () {
    var hookWindow = false;
    var surveyList = [social_network_list_json,
                      norbeck_q1_json,
                      ego_centric_network_matrix_json,
                      aq_json,
                      demographics_json];
    var survey_i = 0;
    var survey_page_i = -1;
    var survey_list_bool = new Array(surveyList.length).fill(true);
    var lastSurveyName = surveyList[surveyList.length - 1].title;

    // parse id in URL
    var userId = '';
    var sid = NaN;
    var parameters = window.location.search.substring(1);
    var param_list = parameters.split(/[&=]/);
    if (param_list.length == 2) {
        userId = param_list[1];
        sid = userId.substring(4);
    } else {
        $('body').empty();
        return;
    }
    if (userId.length < 5 || userId.length > 8 || !userId.startsWith('ucla') ||
        isNaN(sid)) {
        $('body').empty();
        return;
    }
    sid = parseInt(sid);

    // prevent closing window
    window.onbeforeunload = function() {
        if (hookWindow) {
            return 'Do you want to leave this page? Your progress will not be saved.';
        }
    }

    // initialize firebase
    var firebaseUid = null;
    var config = {
        apiKey: "AIzaSyDyzBnPlCKhzrI9RqnhMlRfVBLz2sSs9bM",
        authDomain: "network-survey-f3409.firebaseapp.com",
        databaseURL: "https://network-survey-f3409.firebaseio.com",
        projectId: "network-survey-f3409",
        storageBucket: "",
        messagingSenderId: "631834407302"
    };
    firebase.initializeApp(config);
    firebase.auth().signInAnonymously().catch(function(error) {
        alert('Error: cannot connect to Firebase. Please find the experimenter.\n' + 
              error.code + ': ' + error.message);
    });
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            // User is signed in.
            firebaseUid = user.uid;
            console.log('Signed in as ' + firebaseUid);

            firebase.database().ref(userId).once('value').then(function(snapshot) {
                var writeUser = true;
                if (snapshot.val()) {  // user exists
                    var confirmText = 'It looks like you have already completed this survey. All of your previous data will be erased if you continue. Are you sure you want to continue?';
                    if (!confirm(confirmText)) {
                        writeUser = false;
                        $('body').empty();
                    }
                }
                if (writeUser) {
                    firebase.database().ref(userId + '/').set({
                        firebase_uid: firebaseUid
                    });
                }
            });
        }
    });

    // Survey properties and functions
    var customizedCss = {
        footer: "panel-footer card-footer customized-footer",
        matrixdynamic: {
            button: "btn-sm btn-default"
        }
    };

    function createSurveyModel(surveyJSON) {
        Survey.Survey.cssType = 'bootstrap';
        Survey.defaultBootstrapCss.navigationButton = 'btn btn-success';
        var survey = new Survey.Model(surveyJSON);
        $('#survey-container').Survey({
            model: survey,
            onMatrixCellCreated: onNetworkMatrixCellCreated,
            onPartialSend: sendData,
            onComplete: sendData,
            css: customizedCss,
            completeText: 'Next'
        });
    }

    function processData(survey) {
        var data = {};
        $.each(survey.data, function(name, response) {
            var question_text = survey.getQuestionByName(name);
            if (question_text) {
                data[name] = {
                    text: question_text.title,
                    response: response
                }
            } else {
                data[name] = {response: response};
            }
        });
        return {
            start_time: startTime.toString(),
            end_time: endTime.toString(),
            duration: endTime.getTime() - startTime.getTime(),
            data: data
        };
    }

    function addInfo2NorbeckQ1(survey, friendList) {
        if (friendList.length < 1) {
            survey_list_bool[surveyList.indexOf(norbeck_q1_json)] = false;  // skip it
        }
        else {
            for (var j = 0; j < norbeck_q1_json.pages.length; ++j){
                var matrix_json = norbeck_q1_json.pages[j].elements[0];
                for (var i = 0; i < friendList.length; ++i) {
                    matrix_json.rows.push({
                        'value': (i).toString(),
                        'text': friendList[i].name
                    });
                }
            }
        }
    }

    function addInfo2NetworkMatrix(survey, friendList) {
        if (friendList.length < 2) {
            survey_list_bool[surveyList.indexOf(ego_centric_network_matrix_json)] = false;  // skip it
        }
        else {
            var matrix_json = ego_centric_network_matrix_json.pages[0].elements[0];
            for (var i = 0; i < friendList.length - 1; ++i) {
                matrix_json.columns.push({
                    'name': i.toString(),
                    'title': friendList[i].name,
                    'cellType': 'boolean',
                    "isRequired": true
                });
                matrix_json.rows.push({
                    'value': (i + 1).toString(),
                    'text': friendList[i + 1].name
                });
            }
        }
    }

    function endSurveys() {
        $('body').append($('<p>', {
            text: 'Your response has been recorded. Thank you! Please notify the experimenter.',
            id: 'end-instr'
        }));
        hookWindow = false;
        firebase.auth().currentUser.delete();
    }

    function sendData(survey) {
        if (survey_page_i == survey.currentPageNo) {
            // data has been sent
            return;
        }

        // get data
        endTime = new Date();
        $('#process-modal').modal('show');
        var surveyName = survey.title;
        var data = processData(survey);
        console.log(data);

        // send data to firebase
        var userRef = firebase.database().ref(userId + '/' + (survey_i + 1) + ' ' + surveyName);
        userRef.set(data).then(function() {
            // success
            if (surveyName == lastSurveyName) {
                endSurveys();
            }
            $('#process-modal').modal('hide');
        }, function() {
            $('#process-modal').modal('hide');
            alert('Error: cannot connect to Firebase. Please find the experimenter.');
        });

        // NEXT SURVEY
        if (surveyName == 'Social Network List') {
            var friendList = [];
            for (var i = 0; i < survey.data['social-list'].length; i++) {
                if (survey.data['social-list'][i].hasOwnProperty('name')) {
                    friendList.push(survey.data['social-list'][i]);
                }
            }
            addInfo2NorbeckQ1(survey, friendList);
            addInfo2NetworkMatrix(survey, friendList);
        }
        if (survey.isLastPage) {
            // go to the next survey (if there is one)
            ++survey_i;
            if (survey_i < surveyList.length) {
                survey_page_i = -1;
                while (!survey_list_bool[survey_i]) {
                    survey_i++;
                }
                createSurveyModel(surveyList[survey_i]);
            }
        } else {
            // go to the next page
            survey_page_i = survey.currentPageNo;
            survey.nextPage();
        }
    } // end of function sendData

    function onNetworkMatrixCellCreated(survey, options) {
        // remove a triangle of choices in the social-network matrix
        if (options.question.name != 'social-network') {
            return;
        }
        if (parseInt(options.columnName) >= parseInt(options.row.name)) {
            options.cellQuestion.visible = false;
        }
    }

    // start it
    while (!survey_list_bool[survey_i]) {
        survey_i++;
    }
    createSurveyModel(surveyList[survey_i]);
    hookWindow = true;
    var startTime = new Date();
    var endTime = null;
})();
