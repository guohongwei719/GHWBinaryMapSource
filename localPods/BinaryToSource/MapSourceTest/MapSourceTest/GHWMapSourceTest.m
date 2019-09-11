//
//  GHWMapSourceTest.m
//  MapSourceTest
//
//  Created by 郭宏伟 on 2019/8/25.
//  Copyright © 2019 Jingyao. All rights reserved.
//

#import "GHWMapSourceTest.h"

@implementation GHWMapSourceTest

- (void)testFail {
    NSLog(@"11111");
    NSLog(@"22222");
    NSLog(@"33333");
    NSArray *array = @[@"1"];
    NSLog(@"test = %@", array[2]);
    NSLog(@"44444");
    NSLog(@"55555");
    NSLog(@"66666");
}
- (void)testSuccess {
    NSLog(@"success");
}


@end
