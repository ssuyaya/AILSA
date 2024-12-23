from oscopilot.tool_repository.email_tools.email_fetcher import EmailFetcher

def main():
    """
    Main function to fetch emails using EmailFetcher.
    """
    # 用户配置
    email_address = "yifanwhu523@gmail.com"  # 替换为你的邮箱地址
    password = "yxvworycabmkgxtx"  # 替换为你的邮箱密码
    max_emails = 5  # 要提取的邮件数量

    # 初始化 EmailFetcher
    fetcher = EmailFetcher(email_address=email_address, password=password)

    # 连接到邮箱服务器
    fetcher.connect_to_email_server()

    # 提取邮件并保存到 'emails/' 文件夹
    fetcher.fetch_emails(max_emails=max_emails, output_folder="emails")

    # 关闭邮箱连接
    fetcher.close_connection()


if __name__ == "__main__":
    main()
    
# export PYTHONPATH=/Users/suya/Desktop/oscopilot7607  