import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewAllTemporaryLossApplicationsComponent } from './view-all-temporary-loss-applications.component';

describe('ViewAllTemporaryLossApplicationsComponent', () => {
  let component: ViewAllTemporaryLossApplicationsComponent;
  let fixture: ComponentFixture<ViewAllTemporaryLossApplicationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewAllTemporaryLossApplicationsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewAllTemporaryLossApplicationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
