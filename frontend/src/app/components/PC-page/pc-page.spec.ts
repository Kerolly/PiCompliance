import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PcPage } from './pc-page';

describe('PcPage', () => {
  let component: PcPage;
  let fixture: ComponentFixture<PcPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PcPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PcPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
