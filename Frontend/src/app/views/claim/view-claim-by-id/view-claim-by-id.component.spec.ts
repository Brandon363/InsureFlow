import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewClaimByIdComponent } from './view-claim-by-id.component';

describe('ViewClaimByIdComponent', () => {
  let component: ViewClaimByIdComponent;
  let fixture: ComponentFixture<ViewClaimByIdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewClaimByIdComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewClaimByIdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
