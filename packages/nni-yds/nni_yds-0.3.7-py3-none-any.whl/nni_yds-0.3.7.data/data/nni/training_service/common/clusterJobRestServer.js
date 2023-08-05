'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const express_1 = require("express");
const bodyParser = require("body-parser");
const component = require("../../common/component");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const restServer_1 = require("../../common/restServer");
let ClusterJobRestServer = class ClusterJobRestServer extends restServer_1.RestServer {
    constructor() {
        super();
        this.API_ROOT_URL = '/api/v1/nni-pai';
        this.expId = experimentStartupInfo_1.getExperimentId();
        const basePort = experimentStartupInfo_1.getBasePort();
        assert(basePort && basePort > 1024);
        this.port = basePort + 1;
    }
    get clusterRestServerPort() {
        if (!this.port) {
            throw new Error('PAI Rest server port is undefined');
        }
        return this.port;
    }
    registerRestHandler() {
        this.app.use(bodyParser.json());
        this.app.use(this.API_ROOT_URL, this.createRestHandler());
    }
    createRestHandler() {
        const router = express_1.Router();
        router.use((req, res, next) => {
            this.log.info(`${req.method}: ${req.url}: body:\n${JSON.stringify(req.body, undefined, 4)}`);
            res.setHeader('Content-Type', 'application/json');
            next();
        });
        router.post(`/update-metrics/${this.expId}/:trialId`, (req, res) => {
            try {
                this.log.info(`Get update-metrics request, trial job id is ${req.params.trialId}`);
                this.log.info(`update-metrics body is ${JSON.stringify(req.body)}`);
                this.handleTrialMetrics(req.body.jobId, req.body.metrics);
                res.send();
            }
            catch (err) {
                this.log.error(`json parse metrics error: ${err}`);
                res.status(500);
                res.send(err.message);
            }
        });
        return router;
    }
};
ClusterJobRestServer = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], ClusterJobRestServer);
exports.ClusterJobRestServer = ClusterJobRestServer;
