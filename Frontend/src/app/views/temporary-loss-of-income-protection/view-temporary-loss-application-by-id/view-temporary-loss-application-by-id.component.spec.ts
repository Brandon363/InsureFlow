import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewTemporaryLossApplicationByIdComponent } from './view-temporary-loss-application-by-id.component';

describe('ViewTemporaryLossApplicationByIdComponent', () => {
  let component: ViewTemporaryLossApplicationByIdComponent;
  let fixture: ComponentFixture<ViewTemporaryLossApplicationByIdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewTemporaryLossApplicationByIdComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewTemporaryLossApplicationByIdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
