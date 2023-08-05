import {Component, OnDestroy, OnInit} from "@angular/core";
import {ActivatedRoute} from "@angular/router";
import {NavBackService, TitleBarLink, TitleService} from "@synerty/peek-util";
import {ComponentLifecycleEventEmitter, VortexStatusService} from "@synerty/vortexjs";

@Component({
    selector: "peek-main-title",
    templateUrl: "main-title.component.dweb.html",
    styleUrls: ["main-title.component.dweb.scss"],
    moduleId: module.id
})
export class MainTitleComponent extends ComponentLifecycleEventEmitter implements OnInit {

    private leftLinks = [];
    private rightLinks = [];

    title: string = "Peek";
    isEnabled: boolean = true;
    vortexIsOnline: boolean = false;

    constructor(vortexStatusService: VortexStatusService,
                titleService: TitleService) {
        super();
        this.leftLinks = titleService.leftLinksSnapshot;
        this.rightLinks = titleService.rightLinksSnapshot;

        titleService.title.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.title = v);

        titleService.isEnabled.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.isEnabled = v);

        titleService.leftLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.leftLinks = v);

        titleService.rightLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.rightLinks = v);

        vortexStatusService.isOnline.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.vortexIsOnline = v);

    }

    ngOnInit() {
    }


    // ------------------------------
    // Display methods

    linkTitle(title: TitleBarLink) {
        if (title.badgeCount == null) {
            return title.text;
        }

        if (title.left) {
            return `${title.text} (${title.badgeCount})`;
        }

        return `(${title.badgeCount}) ${title.text}`;

    }
}

