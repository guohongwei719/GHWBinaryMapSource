//
//  ViewController.m
//  GHWBinaryMapSource
//
//  Created by 黑化肥发灰 on 2019/9/11.
//  Copyright © 2019 黑化肥发灰. All rights reserved.
//

#import "ViewController.h"
#import <MapSourceTest/GHWMapSourceTest.h>

@interface ViewController ()
@property (nonatomic, strong) UIButton *tapButton;
@end

@implementation ViewController

#pragma mark - Life Cycle

- (void)viewDidLoad {
    [super viewDidLoad];
    [self configViews];
    [self configData];
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];

}

#pragma mark - Setup View / Data

- (void)configViews {
    [self.view addSubview:self.tapButton];
}

- (void)configData {

}
  
- (void)buttonTap:(id)sender {
    GHWMapSourceTest *test = [[GHWMapSourceTest alloc] init];
    [test testFail];
    
    NSLog(@"ok");
}



#pragma mark - Setter / Getter
- (UIButton *)tapButton {
    if (!_tapButton) {
        _tapButton = [[UIButton alloc] initWithFrame:CGRectMake(30, 100, 250, 50)];
        [_tapButton setTitleColor:[UIColor blueColor] forState:UIControlStateNormal];
        _tapButton.titleLabel.font = [UIFont systemFontOfSize:14];
        _tapButton.backgroundColor = [UIColor lightGrayColor];
        [_tapButton setTitle:@"二进制映射源码测试(点我会 crash 哦)" forState:UIControlStateNormal];
         [_tapButton addTarget:self action:@selector(buttonTap:) forControlEvents:UIControlEventTouchUpInside];
     }
    return _tapButton;
}


#pragma mark - Network





@end
