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
const fs = require("fs");
const path = require("path");
const stream_buffers_1 = require("stream-buffers");
const util_1 = require("util");
const component = require("../common/component");
const utils_1 = require("./utils");
const CRITICAL = 1;
const ERROR = 2;
const WARNING = 3;
const INFO = 4;
const DEBUG = 5;
class BufferSerialEmitter {
    constructor(writable) {
        this.buffer = Buffer.alloc(0);
        this.emitting = false;
        this.writable = writable;
    }
    feed(buffer) {
        this.buffer = Buffer.concat([this.buffer, buffer]);
        if (!this.emitting) {
            this.emit();
        }
    }
    emit() {
        this.emitting = true;
        this.writable.write(this.buffer, () => {
            if (this.buffer.length === 0) {
                this.emitting = false;
            }
            else {
                this.emit();
            }
        });
        this.buffer = Buffer.alloc(0);
    }
}
let Logger = class Logger {
    constructor(fileName) {
        this.DEFAULT_LOGFILE = path.join(utils_1.getLogDir(), 'nnimanager.log');
        this.level = DEBUG;
        let logFile = fileName;
        if (logFile === undefined) {
            logFile = this.DEFAULT_LOGFILE;
        }
        this.writable = fs.createWriteStream(logFile, {
            flags: 'a+',
            encoding: 'utf8',
            autoClose: true
        });
        this.bufferSerialEmitter = new BufferSerialEmitter(this.writable);
    }
    close() {
        this.writable.destroy();
    }
    debug(...param) {
        if (this.level >= DEBUG) {
            this.log('DEBUG', param);
        }
    }
    info(...param) {
        if (this.level >= INFO) {
            this.log('INFO', param);
        }
    }
    warning(...param) {
        if (this.level >= WARNING) {
            this.log('WARNING', param);
        }
    }
    error(...param) {
        if (this.level >= ERROR) {
            this.log('ERROR', param);
        }
    }
    critical(...param) {
        this.log('CRITICAL', param);
    }
    log(level, param) {
        const buffer = new stream_buffers_1.WritableStreamBuffer();
        buffer.write(`[${(new Date()).toISOString()}] ${level} `);
        buffer.write(util_1.format.apply(null, param));
        buffer.write('\n');
        buffer.end();
        this.bufferSerialEmitter.feed(buffer.getContents());
    }
};
Logger = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [String])
], Logger);
exports.Logger = Logger;
function getLogger(fileName) {
    component.Container.bind(Logger).provider({
        get: () => new Logger(fileName)
    });
    return component.get(Logger);
}
exports.getLogger = getLogger;
