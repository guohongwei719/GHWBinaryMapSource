//
//  GHWFrameworkTest.m
//  GHWTestFramework
//
//  Created by 郭宏伟 on 2019/8/20.
//  Copyright © 2019 Jingyao. All rights reserved.
//

#import "GHWFrameworkTest.h"

@implementation GHWFrameworkTest

- (void)testFail {
    NSArray *array = @[@"1"];
    NSLog(@"test = %@", array[2]);
    NSLog(@"11111");
    NSLog(@"22222");
    NSLog(@"33333");
}

- (void)testSuccess {
    NSLog(@"success");
}
@end
