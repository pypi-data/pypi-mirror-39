import {Component, OnInit} from "@angular/core";
import {TitleService} from "@synerty/peek-util";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";

import {
    DeviceNavService,
    DeviceServerService,
    DeviceTupleService,
    EnrolDeviceAction,
    ServerInfoTuple
} from "@peek/peek_core_device/_private";

import {DeviceInfoTuple} from "@peek/peek_core_device";
import {DeviceTypeEnum} from "@peek/peek_core_device/_private/hardware-info/hardware-info.abstract";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";


@Component({
    selector: 'peek-plugin-diagram-cfg-connect',
    templateUrl: 'connect.component.web.html',
    moduleId: module.id
})
export class ConnectComponent extends ComponentLifecycleEventEmitter implements OnInit {

    server: ServerInfoTuple = new ServerInfoTuple();

    httpPortStr: string = '8000';
    websocketPortStr: string = '8001';

    deviceType: DeviceTypeEnum;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private titleService: TitleService,
                private tupleService: DeviceTupleService,
                private deviceServerService: DeviceServerService) {
        super();


        this.deviceType = this.tupleService.hardwareInfo.deviceType();

        this.deviceServerService.connInfoObserver
            .takeUntil(this.onDestroyEvent)
            .subscribe((info: ServerInfoTuple) => {
                this.server = info;
            });

        this.server = this.deviceServerService.connInfo;
    }

    ngOnInit() {

        switch (this.deviceType) {
            case DeviceTypeEnum.MOBILE_WEB:
            case DeviceTypeEnum.DESKTOP_WEB:
                // If this is a web service, always use the host from the URL
                this.server = this.deviceServerService.extractHttpDetails();
                this.httpPortStr = this.server.httpPort.toString();
                break;

            default:
                break;
        }

    }


    connectEnabled(): boolean {

        if (this.server != null) {
            if (this.server.host == null || !this.server.host.length)
                return false;

            if (!parseInt(this.websocketPortStr))
                return false;

            if (!parseInt(this.httpPortStr))
                return false;

        }
        return true;
    }

    saveClicked() {
        try {
            this.server.httpPort = parseInt(this.httpPortStr);
            this.server.websocketPort = parseInt(this.websocketPortStr);

        } catch (e) {
            this.balloonMsg.showError("Port numbers must be integers.");
            return;
        }

        this.deviceServerService.setServer(this.server)
            .then(() => {
                this.balloonMsg.showSuccess("Peek server has been updated");
            });

    }

    setUseSsl(val:boolean) {
        this.server.useSsl = val;
    }


}