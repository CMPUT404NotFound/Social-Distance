import React, { useState } from 'react';
import { Row, Col, Upload, Button, message, Radio, Input, Space } from 'antd';
import 'antd/dist/antd.css';
import { UploadOutlined } from '@ant-design/icons';
import TextArea from "rc-textarea";
let ReactCommonmark = require('react-commonmark');

const Uploader = () => {
    const props = {
      beforeUpload: file => {
        if (file.type !== 'image/png') {
          message.error(`${file.name} is not a png file`);
        }
        return file.type === 'image/png' ? true : Upload.LIST_IGNORE;
      },
      onChange: info => {
        console.log(info.fileList);
      },
    };
    return (
      <Upload {...props}>
        <Button icon={<UploadOutlined />}>Upload png only</Button>
      </Upload>
    );
  };

class ShareTo extends React.Component {
    state = {
        value: 1,
    };

    onChange = e => {
        console.log('radio checked', e.target.value);
        this.setState({
        value: e.target.value,
        });
    };

    render() {
        const { value } = this.state;
        return (
        <Radio.Group onChange={this.onChange} value={value}>
            <Space direction="vertical">
                <Radio value={1}>Public</Radio>
                <Radio value={2}>Friends Only</Radio>
                <Radio value={3}>
                    Specific Authors Only
                    {value === 3 ? <Input style={{ width: 100, marginLeft: 10 }} /> : null}
                </Radio>
                <Radio value={4}>More...</Radio>
            </Space>
        </Radio.Group>
        );
    }
}

export default class CreatePost extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      markdown: "# Type your heart out~",
    };
  }

  updateMarkdown(markdown) {
    this.setState({ markdown });
  }

  render() {

    var inputStyle = {
        width: "500px",
        height: "50vh",
        marginLeft: "auto",
        marginRight: "auto",
        padding:"10px"
      };

    var outputStyle = {
      width: "400px",
      height: "50vh",
      backgroundColor: "#DCDCDC",
      marginLeft: "auto",
      marginRight: "auto",
      padding:"10px"
    };

    return (
      <>
        <Row>
        <Col span={24}>
            <h1>Create a Post</h1>
        </Col>
      </Row>
      <Row>
        <Col span={12}>
            <h2>Enter your text</h2>
            <TextArea style={inputStyle}
                      value={this.state.markdown}
                      onChange={(e) => {
                        this.updateMarkdown(e.target.value);
                      }}>        
            </TextArea>
        </Col>
        <Col span={12}>
            <h2>Preview your post</h2>
            <ReactCommonmark source={this.state.markdown} />
            
        </Col>
      </Row>
      <Row>
        <Col span={24}>
            <h3>...or upload your images</h3>
            <Uploader />
        </Col>
      </Row>
      <Row>
        <Col span={24}>
            <h2>Share your post to: </h2>
            <ShareTo />
            <Button type="primary" shape="round">Download</Button>
        </Col>
      </Row>
    </>
    );
  }
}