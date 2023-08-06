"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
var RestServer_1;
'use strict';
const bodyParser = require("body-parser");
const express = require("express");
const ts_deferred_1 = require("ts-deferred");
const component = require("../common/component");
const log_1 = require("../common/log");
const restHandler_1 = require("./restHandler");
let RestServer = RestServer_1 = class RestServer {
    constructor() {
        this.API_ROOT_URL = '/api/v1/nni';
        this.hostName = '0.0.0.0';
        this.port = RestServer_1.DEFAULT_PORT;
        this.app = express();
        this.log = log_1.getLogger();
    }
    get endPoint() {
        return `http://${this.hostName}:${this.port}`;
    }
    start(port, hostName) {
        if (this.startTask !== undefined) {
            return this.startTask.promise;
        }
        this.startTask = new ts_deferred_1.Deferred();
        this.registerRestHandler();
        if (hostName) {
            this.hostName = hostName;
        }
        if (port) {
            this.port = port;
        }
        this.server = this.app.listen(this.port, this.hostName).on('listening', () => {
            this.startTask.resolve();
        }).on('error', (e) => {
            this.startTask.reject(e);
        });
        return this.startTask.promise;
    }
    stop() {
        if (this.stopTask !== undefined) {
            return this.stopTask.promise;
        }
        this.stopTask = new ts_deferred_1.Deferred();
        if (this.startTask === undefined) {
            this.stopTask.resolve();
            return this.stopTask.promise;
        }
        else {
            this.startTask.promise.then(() => {
                this.server.close().on('close', () => {
                    this.log.info('Rest server stopped.');
                    this.stopTask.resolve();
                }).on('error', (e) => {
                    this.log.error(`Error occurred stopping Rest server: ${e.message}`);
                    this.stopTask.reject();
                });
            }, () => {
                this.stopTask.resolve();
            });
        }
        return this.stopTask.promise;
    }
    registerRestHandler() {
        this.app.use(bodyParser.json());
        this.app.use(this.API_ROOT_URL, restHandler_1.createRestHandler(this));
    }
};
RestServer.DEFAULT_PORT = 51188;
RestServer = RestServer_1 = __decorate([
    component.Singleton
], RestServer);
exports.RestServer = RestServer;
