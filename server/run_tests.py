import dev_appserver
import nose


if __name__ == "__main__":
  dev_appserver.fix_sys_path()

  nose.main()
