import { TestBed } from '@angular/core/testing';

import { FunctionSelectionService } from './function-selection-service';

describe('FunctionSelectionService', () => {
  let service: FunctionSelectionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FunctionSelectionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
