import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewClaimsByUserIdComponent } from './view-claims-by-user-id.component';

describe('ViewClaimsByUserIdComponent', () => {
  let component: ViewClaimsByUserIdComponent;
  let fixture: ComponentFixture<ViewClaimsByUserIdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewClaimsByUserIdComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewClaimsByUserIdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
