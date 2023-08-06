'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const path = require("path");
const component = require("../common/component");
const datastore_1 = require("../common/datastore");
const errors_1 = require("../common/errors");
const experimentStartupInfo_1 = require("../common/experimentStartupInfo");
const log_1 = require("../common/log");
const manager_1 = require("../common/manager");
const restValidationSchemas_1 = require("./restValidationSchemas");
const tensorboard_1 = require("./tensorboard");
const expressJoi = require('express-joi-validator');
class NNIRestHandler {
    constructor(rs) {
        this.nniManager = component.get(manager_1.Manager);
        this.restServer = rs;
        this.tb = new tensorboard_1.TensorBoard();
        this.log = log_1.getLogger();
    }
    createRestHandler() {
        const router = express_1.Router();
        router.use((req, res, next) => {
            this.log.info(`${req.method}: ${req.url}: body:\n${JSON.stringify(req.body, undefined, 4)}`);
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
            res.header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS');
            res.setHeader('Content-Type', 'application/json');
            next();
        });
        this.checkStatus(router);
        this.getExperimentProfile(router);
        this.updateExperimentProfile(router);
        this.startExperiment(router);
        this.getTrialJobStatistics(router);
        this.setClusterMetaData(router);
        this.listTrialJobs(router);
        this.getTrialJob(router);
        this.addTrialJob(router);
        this.cancelTrialJob(router);
        this.getMetricData(router);
        this.getExample(router);
        this.getTriedParameters(router);
        this.startTensorBoard(router);
        this.stopTensorBoard(router);
        router.use((err, req, res, next) => {
            if (err.isBoom) {
                this.log.error(err.output.payload);
                return res.status(err.output.statusCode).json(err.output.payload);
            }
        });
        return router;
    }
    handle_error(err, res, isFatal = false) {
        if (err instanceof errors_1.NNIError && err.name === errors_1.NNIErrorNames.NOT_FOUND) {
            res.status(404);
        }
        else {
            res.status(500);
        }
        res.send({
            error: err.message
        });
        if (isFatal) {
            this.log.critical(err);
            process.exit(1);
        }
        this.log.error(err);
    }
    checkStatus(router) {
        router.get('/check-status', (req, res) => {
            const ds = component.get(datastore_1.DataStore);
            ds.init().then(() => {
                res.send(this.nniManager.getStatus());
            }).catch(async (err) => {
                this.handle_error(err, res);
                this.log.error(err.message);
                this.log.error(`Database initialize failed, stopping rest server...`);
                await this.restServer.stop();
            });
        });
    }
    getExperimentProfile(router) {
        router.get('/experiment', (req, res) => {
            this.nniManager.getExperimentProfile().then((profile) => {
                res.send(profile);
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    updateExperimentProfile(router) {
        router.put('/experiment', expressJoi(restValidationSchemas_1.ValidationSchemas.UPDATEEXPERIMENT), (req, res) => {
            this.nniManager.updateExperimentProfile(req.body, req.query.update_type).then(() => {
                res.send();
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    startExperiment(router) {
        router.post('/experiment', expressJoi(restValidationSchemas_1.ValidationSchemas.STARTEXPERIMENT), (req, res) => {
            if (experimentStartupInfo_1.isNewExperiment()) {
                this.nniManager.startExperiment(req.body).then((eid) => {
                    res.send({
                        experiment_id: eid
                    });
                }).catch((err) => {
                    this.handle_error(err, res);
                });
            }
            else {
                this.nniManager.resumeExperiment().then(() => {
                    res.send();
                }).catch((err) => {
                    this.handle_error(err, res);
                });
            }
        });
    }
    getTrialJobStatistics(router) {
        router.get('/job-statistics', (req, res) => {
            this.nniManager.getTrialJobStatistics().then((statistics) => {
                res.send(statistics);
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    setClusterMetaData(router) {
        router.put('/experiment/cluster-metadata', expressJoi(restValidationSchemas_1.ValidationSchemas.SETCLUSTERMETADATA), async (req, res) => {
            const metadata = req.body;
            const keys = Object.keys(metadata);
            try {
                for (const key of keys) {
                    await this.nniManager.setClusterMetadata(key, JSON.stringify(metadata[key]));
                }
                res.send();
            }
            catch (err) {
                this.handle_error(err, res, true);
            }
        });
    }
    listTrialJobs(router) {
        router.get('/trial-jobs', (req, res) => {
            this.nniManager.listTrialJobs(req.query.status).then((jobInfos) => {
                jobInfos.forEach((trialJob) => {
                    this.setErrorPathForFailedJob(trialJob);
                });
                res.send(jobInfos);
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    getTrialJob(router) {
        router.get('/trial-jobs/:id', (req, res) => {
            this.nniManager.getTrialJob(req.params.id).then((jobDetail) => {
                const jobInfo = this.setErrorPathForFailedJob(jobDetail);
                res.send(jobInfo);
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    addTrialJob(router) {
        router.post('/trial-jobs', async (req, res) => {
            this.nniManager.addCustomizedTrialJob(JSON.stringify(req.body)).then(() => {
                res.send();
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    cancelTrialJob(router) {
        router.delete('/trial-jobs/:id', async (req, res) => {
            this.nniManager.cancelTrialJobByUser(req.params.id).then(() => {
                res.send();
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    getMetricData(router) {
        router.get('/metric-data/:job_id*?', async (req, res) => {
            this.nniManager.getMetricData(req.params.job_id, req.query.type).then((metricsData) => {
                res.send(metricsData);
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    startTensorBoard(router) {
        router.post('/tensorboard', expressJoi(restValidationSchemas_1.ValidationSchemas.STARTTENSORBOARD), async (req, res) => {
            const jobIds = req.query.job_ids.split(',');
            const tensorboardCmd = req.query.tensorboard_cmd;
            this.tb.startTensorBoard(jobIds, tensorboardCmd).then((endPoint) => {
                res.send({ endPoint: endPoint });
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    stopTensorBoard(router) {
        router.delete('/tensorboard', expressJoi(restValidationSchemas_1.ValidationSchemas.STOPTENSORBOARD), async (req, res) => {
            const endPoint = req.query.endpoint;
            this.tb.stopTensorBoard(endPoint).then(() => {
                res.send();
            }).catch((err) => {
                this.handle_error(err, res);
            });
        });
    }
    getExample(router) {
        router.get('/example', async (req, res) => {
        });
    }
    getTriedParameters(router) {
        router.get('/tried-parameters', async (req, res) => {
        });
    }
    setErrorPathForFailedJob(jobInfo) {
        if (jobInfo === undefined || jobInfo.status !== 'FAILED' || jobInfo.logPath === undefined) {
            return jobInfo;
        }
        jobInfo.stderrPath = path.join(jobInfo.logPath, 'stderr');
        return jobInfo;
    }
}
function createRestHandler(rs) {
    const handler = new NNIRestHandler(rs);
    return handler.createRestHandler();
}
exports.createRestHandler = createRestHandler;
