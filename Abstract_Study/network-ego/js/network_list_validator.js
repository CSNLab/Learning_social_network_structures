'use strict';

var NetworkListValidator = (function (_super) {
    Survey.__extends(NetworkListValidator, _super);

    function NetworkListValidator() {
        _super.call(this);
    }

    NetworkListValidator.prototype.getType = function () {
        return "networklistvalidator";
    };

    NetworkListValidator.prototype.validate = function (data) {
        for (var i = 0; i < data.length; ++i) {
            var cols_filled = 0;
            cols_filled += data[i].hasOwnProperty('name') ? 1: 0;
            cols_filled += data[i].hasOwnProperty('gender') ? 1: 0;
            cols_filled += data[i].hasOwnProperty('relationship') ? 1: 0;
            if (cols_filled > 0 && cols_filled < 3) {
                // report an error
                return new Survey.ValidatorResult(null, new Survey.CustomError(this.getErrorText(i + 1)));
            }
        }
        // no error
        return null;
    };

    // the default error text. It shows if user do not set the 'text' property
    NetworkListValidator.prototype.getDefaultErrorText = function (row) {
        var row_name = row + (row == 1 ? 'st' : (row == 2 ? 'nd' : 'th'));
        return "Please complete the " + row_name + " row or remove it.";
    }

    return NetworkListValidator;
})(Survey.SurveyValidator);

Survey.NetworkListValidator = NetworkListValidator;

// add into survey Json metaData
Survey
    .JsonObject
    .metaData
    .addClass("networklistvalidator", [], function () {
        return new NetworkListValidator();
    }, "surveyvalidator");
