import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExtractTemporaryLossApplicationComponent } from './extract-temporary-loss-application.component';

describe('ExtractTemporaryLossApplicationComponent', () => {
  let component: ExtractTemporaryLossApplicationComponent;
  let fixture: ComponentFixture<ExtractTemporaryLossApplicationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExtractTemporaryLossApplicationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExtractTemporaryLossApplicationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
