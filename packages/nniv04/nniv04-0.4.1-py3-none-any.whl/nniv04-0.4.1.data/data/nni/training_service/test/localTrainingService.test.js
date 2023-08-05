'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const localTrainingService_1 = require("../local/localTrainingService");
const component = require("../../common/component");
describe('Unit Test for LocalTrainingService', () => {
    let trainingService;
    beforeEach(async () => {
        trainingService = component.get(localTrainingService_1.LocalTrainingService);
    });
});
