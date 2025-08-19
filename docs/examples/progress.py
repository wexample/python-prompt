from wexample_prompt.common.io_manager import IoManager

if __name__ == "__main__":
    demo_io = IoManager()

    demo_io.echo(f'This is a {"long " * 100}message')

    demo_io.progress(
        label='TODO test progress',
        total=1000,
        current=0
    )
