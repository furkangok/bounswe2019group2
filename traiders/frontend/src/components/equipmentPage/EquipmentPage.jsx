import React, { Component } from 'react';

import Page from '../page/Page';
import CustomTable from '../customTable/CustomTable';
import Comment from '../comment/CommentContainer';
import AddComment from '../addComment/AddCommentContainer';
import './equipment-page.scss';

class EquipmentPage extends Component {
  componentWillMount() {
    const { match, getParities } = this.props;
    const { base } = match.params;
    getParities();

    const { getEquipmentComments, getEquipment } = this.props;
    getEquipmentComments(base);
    getEquipment(base);
  }

  render() {
    const { comments, match } = this.props;
    const { base } = match.params;
    let { parityList } = this.props;
    if (parityList) {
      parityList = parityList.filter((parity) => {
        return parity.target_equipment.symbol === base;
      });
    }

    return (
      <Page>
        <div className="container">
          <div>
            <CustomTable parityList={parityList} />
          </div>
          <div>
            {comments &&
              comments.map((comment) => (
                <Comment
                  submitUrl="https://api.traiders.tk/comments/equipment/"
                  author={comment.user.username}
                  content={comment.content}
                  createdAt={comment.created_at.substring(0, 10)}
                  image={comment.image}
                  commentId={comment.id}
                  equipment={comment.equipment}
                  authorURL={comment.user.url}
                  avatarValue={comment.user.avatar}
                  numberofLikes={comment.num_likes}
                  isLiked={comment.is_liked}
                />
              ))}
          </div>
          <div>
            <AddComment submitUrl="https://api.traiders.tk/comments/equipment/" />
          </div>
        </div>
      </Page>
    );
  }
}
export default EquipmentPage;
