import React from "react";
import { Row, Col } from "antd";
import { UserOutlined, HeartOutlined, CommentOutlined, ShareAltOutlined } from "@ant-design/icons";
let ReactCommonmark = require("react-commonmark");

const Post = () => {
    var sample_text = `# Spooky, scary skeletons
    ## send shivers down your spine
    `;
    var sample_author = "dokyeom";

    return (
        <div className="post_container">
                <Row justify="center">
                    <Col span={10}>
                        <UserOutlined/>
                        <p>{sample_author}</p>
                    </Col>
                </Row>
                <Row justify="center">
                    <Col span={10}>
                        <ReactCommonmark source={sample_text} />
                    </Col>
                </Row>
                <Row justify="center">
                    <Col span={10}>
                        <HeartOutlined />
                        <CommentOutlined />
                        <ShareAltOutlined />
                    </Col>
                </Row>
        </div>
    )
};

export default Post;
